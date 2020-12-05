"""Database models."""

import typing
import time
from pynamodb import models, attributes

from ... import config
from . import exceptions


TPackageStoreSub = str
TPackageStoreSpecId = str
TPackageStoreVersion = str
TPackageStoreUpdatedAt = str
TPackageStoreModelCount = int
TPackageStoreUpdatedAtSpecId = str


class PackageStorage(models.Model):
    """
    Information about a package.

    Attrs:
        sub: Unique identifier for a customer
        spec_id: Unique identifier for a spec for a package
        version: The version of a spec for a package
        updated_at: The last time the spec version was updated in integer seconds since
            epoch stored as a string or 'latest' for the copy of the latest version of
            the spec.
        model_count: The number of 'x-tablename' and 'x-inherits' in a spec
        updated_at_spec_id: Combination of 'updated_at' and 'spec_id' separeted with #

    """

    class Meta:
        table_name = config.get_env().package_storage_table_name

        if config.get_env().stage == config.Stage.TEST:
            host = "http://localhost:8000"
            aws_access_key_id = "invalid id"
            aws_secret_access_key = "invalid key"

    sub = attributes.UnicodeAttribute(hash_key=True)
    spec_id = attributes.UnicodeAttribute()
    version = attributes.UnicodeAttribute()
    updated_at = attributes.UnicodeAttribute()
    UPDATED_AT_LATEST = "latest"
    model_count = attributes.NumberAttribute()
    updated_at_spec_id = attributes.UnicodeAttribute(range_key=True)

    @classmethod
    def count_customer_models(cls, *, sub: TPackageStoreSub) -> int:
        """
        Count the number of models on the latest specs for a customer.

        Filters for a particular customer and updated_at_spec_id to start with
        'latest#' and sums over model_count.

        Args:
            sub: Unique identifier for the customer.

        Returns:
            The sum of the model count on the latest version of each unique spec for
            the customer.

        """
        return sum(
            map(
                lambda item: int(item.model_count),
                cls.query(
                    sub,
                    cls.updated_at_spec_id.startswith(f"{cls.UPDATED_AT_LATEST}#"),
                ),
            )
        )

    @classmethod
    def calc_updated_at_spec_id(
        cls, *, updated_at: TPackageStoreUpdatedAt, spec_id: TPackageStoreSpecId
    ) -> TPackageStoreUpdatedAtSpecId:
        """
        Calculate the updated_at_spec_id value.

        Args:
            updated_at: The value for updated_at
            spec_id: The value for spec_id

        Returns:
            The value for updated_at_spec_id

        """
        # Zero pad updated_at if it is not latest
        if updated_at != cls.UPDATED_AT_LATEST:
            updated_at = updated_at.zfill(20)

        return f"{updated_at}#{spec_id}"

    @classmethod
    def create_update_item(
        cls,
        *,
        sub: TPackageStoreSub,
        spec_id: TPackageStoreSpecId,
        version: TPackageStoreVersion,
        model_count: TPackageStoreModelCount,
    ) -> None:
        """
        Create or update an item.

        Creates or updates 2 items in the database. The updated_at attribute for the
        first is calculated based on seconds since epoch and for the second is set to
        'latest'. Also computes the sort key updated_at_spec_id based on updated_at and
        spec_id.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.
            version: The version of the spec.
            model_count: The number of models in the spec.

        """
        # Write item
        updated_at = str(int(time.time()))
        updated_at_spec_id = cls.calc_updated_at_spec_id(
            updated_at=updated_at, spec_id=spec_id
        )
        item = cls(
            sub=sub,
            spec_id=spec_id,
            version=version,
            model_count=model_count,
            updated_at=updated_at,
            updated_at_spec_id=updated_at_spec_id,
        )
        item.save()

        # Write latest item
        updated_at_latest = cls.UPDATED_AT_LATEST
        updated_at_spec_id_latest = cls.calc_updated_at_spec_id(
            updated_at=updated_at_latest, spec_id=spec_id
        )
        item_latest = cls(
            sub=sub,
            spec_id=spec_id,
            version=version,
            model_count=model_count,
            updated_at=updated_at_latest,
            updated_at_spec_id=updated_at_spec_id_latest,
        )
        item_latest.save()

    @classmethod
    def get_latest_version(
        cls, *, sub: TPackageStoreSub, spec_id: TPackageStoreSpecId
    ) -> TPackageStoreVersion:
        """
        Get the latest version for a spec.

        Raises NotFoundError if the spec is not found in the database.

        Calculates updated_at_spec_id by setting updated_at to latest and using the
        spec_id. Tries to retrieve an item for a customer based on the sort key.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        Returns:
            The latest version of the spec.

        """
        try:
            item = cls.get(
                hash_key=sub,
                range_key=cls.calc_updated_at_spec_id(
                    updated_at=cls.UPDATED_AT_LATEST, spec_id=spec_id
                ),
            )
            return item.version
        except cls.DoesNotExist as exc:
            raise exceptions.NotFoundError(
                f"the spec {spec_id} does not exist for customer {sub}"
            ) from exc

    @classmethod
    def list_specs(cls, *, sub: TPackageStoreSub) -> typing.List[TPackageStoreSpecId]:
        """
        List all available specs for a customer.

        Filters for a customer and for updated_at_spec_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of all spec id for the customer.

        """
        return list(
            map(
                lambda item: item.spec_id,
                cls.query(
                    sub,
                    cls.updated_at_spec_id.startswith(f"{cls.UPDATED_AT_LATEST}#"),
                ),
            )
        )

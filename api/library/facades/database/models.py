"""Database models."""

import typing
import time
from pynamodb import models, attributes, indexes

from ... import config
from . import exceptions
from . import types


TPackageStoreSub = types.TSub
TPackageStoreSpecId = types.TSpecId
TPackageStoreUpdatedAt = types.TUpdatedAt

TPackageStoreVersion = types.TVersion
TPackageStoreTitle = types.TTitle
TPackageStoreDescription = types.TDescription
TPackageStoreModelCount = types.TModelCount

TPackageStoreUpdatedAtSpecId = str
TPackageStoreSpecIdUpdatedAt = str


class TPackageStoreIndexValues(typing.NamedTuple):
    """The index values for PackageStore."""

    updated_at_spec_id: TPackageStoreUpdatedAtSpecId
    spec_id_updated_at: TPackageStoreSpecIdUpdatedAt


class SpecIdUpdatedAtIndex(indexes.LocalSecondaryIndex):
    """Local secondary index for querying based on spec_id."""

    class Meta:
        projection = indexes.AllProjection()
        index_name = config.get_env().package_database_index_name

        if config.get_env().stage == config.Stage.TEST:
            host = "http://localhost:8000"

    sub = attributes.UnicodeAttribute(hash_key=True)
    spec_id_updated_at = attributes.UnicodeAttribute(range_key=True)


class PackageStorage(models.Model):
    """
    Information about a package.

    Attrs:
        UPDATED_AT_LATEST: Constant for what to set updated_at to to indicate it is the
            latest record

        sub: Unique identifier for a customer
        spec_id: Unique identifier for a spec for a package
        updated_at: The last time the spec version was updated in integer seconds since
            epoch stored as a string or 'latest' for the copy of the latest version of
            the spec.

        version: The version of a spec for a package
        title: The title of a spec
        description: The description of a spec
        model_count: The number of 'x-tablename' and 'x-inherits' in a spec

        updated_at_spec_id: Combination of 'updated_at' and 'spec_id' separeted with #
        spec_id_updated_at: Combination of 'spec_id' and 'updated_at' separeted with #

        spec_id_updated_at_index: Index for querying spec_id_updated_at efficiently

    """

    UPDATED_AT_LATEST = "latest"

    class Meta:
        table_name = config.get_env().package_database_table_name

        if config.get_env().stage == config.Stage.TEST:
            host = "http://localhost:8000"

    sub = attributes.UnicodeAttribute(hash_key=True)
    spec_id = attributes.UnicodeAttribute()
    updated_at = attributes.UnicodeAttribute()

    version = attributes.UnicodeAttribute()
    title = attributes.UnicodeAttribute(null=True)
    description = attributes.UnicodeAttribute(null=True)
    model_count = attributes.NumberAttribute()

    updated_at_spec_id = attributes.UnicodeAttribute(range_key=True)
    spec_id_updated_at = attributes.UnicodeAttribute()

    spec_id_updated_at_index = SpecIdUpdatedAtIndex()

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
    def calc_index_values(
        cls, *, updated_at: TPackageStoreUpdatedAt, spec_id: TPackageStoreSpecId
    ) -> TPackageStoreIndexValues:
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

        return TPackageStoreIndexValues(
            updated_at_spec_id=f"{updated_at}#{spec_id}",
            spec_id_updated_at=f"{spec_id}#{updated_at}",
        )

    @classmethod
    def create_update_item(
        cls,
        *,
        sub: TPackageStoreSub,
        spec_id: TPackageStoreSpecId,
        version: TPackageStoreVersion,
        model_count: TPackageStoreModelCount,
        title: TPackageStoreTitle = None,
        description: TPackageStoreDescription = None,
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
            title: The title of a spec
            description: The description of a spec

        """
        # Write item
        updated_at = str(int(time.time()))
        index_values = cls.calc_index_values(updated_at=updated_at, spec_id=spec_id)
        item = cls(
            sub=sub,
            spec_id=spec_id,
            updated_at=updated_at,
            version=version,
            title=title,
            description=description,
            model_count=model_count,
            updated_at_spec_id=index_values.updated_at_spec_id,
            spec_id_updated_at=index_values.spec_id_updated_at,
        )
        item.save()

        # Write latest item
        updated_at_latest = cls.UPDATED_AT_LATEST
        index_values_latest = cls.calc_index_values(
            updated_at=updated_at_latest, spec_id=spec_id
        )
        item_latest = cls(
            sub=sub,
            spec_id=spec_id,
            version=version,
            updated_at=updated_at_latest,
            title=title,
            description=description,
            model_count=model_count,
            updated_at_spec_id=index_values_latest.updated_at_spec_id,
            spec_id_updated_at=index_values_latest.spec_id_updated_at,
        )
        item_latest.save()

    @classmethod
    def get_latest_spec_version(
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
                range_key=cls.calc_index_values(
                    updated_at=cls.UPDATED_AT_LATEST, spec_id=spec_id
                ).updated_at_spec_id,
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

    @classmethod
    def delete_spec(
        cls, *, sub: TPackageStoreSub, spec_id: TPackageStoreSpecId
    ) -> None:
        """
        Delete a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        """
        items = cls.spec_id_updated_at_index.query(
            sub, cls.spec_id_updated_at.startswith(f"{spec_id}#")
        )
        with cls.batch_write() as batch:
            for item in items:
                batch.delete(item)

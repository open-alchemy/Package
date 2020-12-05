"""Database models."""

import time
from pynamodb import models, attributes

from ... import config


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

    sub = attributes.UnicodeAttribute(hash_key=True)
    spec_id = attributes.UnicodeAttribute()
    version = attributes.UnicodeAttribute()
    updated_at = attributes.UnicodeAttribute()
    UPDATED_AT_LATEST = "latest"
    model_count = attributes.NumberAttribute()
    updated_at_spec_id = attributes.UnicodeAttribute(range_key=True)

    @classmethod
    def count_customer_models(cls, *, sub: str) -> int:
        """
        Count the number of models on the latest specs for a customer.

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

    @staticmethod
    def calc_updated_at_spec_id(*, updated_at: str, spec_id: str) -> str:
        """
        Calculate the updated_at_spec_id value.

        Args:
            updated_at: The value for updated_at
            spec_id: The value for spec_id

        Returns:
            The value for updated_at_spec_id

        """
        return f"{updated_at}#{spec_id}"

    @classmethod
    def create_update_item(
        cls, *, sub: str, spec_id: str, version: str, model_count: int
    ) -> None:
        """
        Create or update an item.

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

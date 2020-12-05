"""Database models."""

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

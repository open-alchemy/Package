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
    model_count = attributes.NumberAttribute()
    updated_at_spec_id = attributes.UnicodeAttribute(range_key=True)

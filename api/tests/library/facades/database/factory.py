"""Model factories."""

import factory

from library.facades.database import models


def package_store_calc_spec_id(n: int) -> str:
    """Calculate the spec_id."""
    return f"spec id {n}"


def package_store_calc_updated_at(n: int) -> str:
    """Calculate the spec_id."""
    return str((n + 1) * 10 + 1)


class PackageStorageFactory(factory.Factory):
    """Factory for PackageStorage model."""

    class Meta:
        model = models.PackageStorage

    sub = factory.Sequence(lambda n: f"sub {n}")
    spec_id = factory.Sequence(package_store_calc_spec_id)
    version = factory.Sequence(lambda n: f"version {n}")
    updated_at = factory.Sequence(package_store_calc_updated_at)
    model_count = factory.Sequence(lambda n: (n + 1) * 10 + 2)
    updated_at_spec_id = factory.Sequence(
        lambda n: f"{package_store_calc_updated_at(n)}#{package_store_calc_spec_id(n)}"
    )

"""Model factories."""

import factory
from library.facades.database import models


def package_store_calc_spec_id(number: int) -> str:
    """Calculate the spec_id."""
    return f"spec id {number}"


def package_store_calc_updated_at(number: int) -> str:
    """Calculate the spec_id."""
    return str((number + 1) * 10 + 1)


class PackageStorageFactory(factory.Factory):
    """Factory for PackageStorage model."""

    class Meta:
        """Meta class."""

        model = models.PackageStorage

    sub = factory.Sequence(lambda n: f"sub {n}")
    spec_id = factory.Sequence(package_store_calc_spec_id)
    updated_at = factory.Sequence(package_store_calc_updated_at)

    version = factory.Sequence(lambda n: f"version {n}")
    title = factory.Sequence(lambda n: f"title {n}")
    description = factory.Sequence(lambda n: f"description {n}")
    model_count = factory.Sequence(lambda n: (n + 1) * 10 + 2)

    updated_at_spec_id = factory.Sequence(
        lambda n: models.PackageStorage.calc_index_values(
            updated_at=package_store_calc_updated_at(n),
            spec_id=package_store_calc_spec_id(n),
        ).updated_at_spec_id
    )
    spec_id_updated_at = factory.Sequence(
        lambda n: models.PackageStorage.calc_index_values(
            updated_at=package_store_calc_updated_at(n),
            spec_id=package_store_calc_spec_id(n),
        ).spec_id_updated_at
    )

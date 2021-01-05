"""Model factories."""

import factory

from . import models


def spec_calc_id(number: int) -> str:
    """Calculate the id."""
    return f"spec id {number}"


def spec_calc_updated_at(number: int) -> str:
    """Calculate updated at."""
    return str((number + 1) * 10 + 1)


class SpecFactory(factory.Factory):
    """Factory for Spec model."""

    class Meta:
        """Meta class."""

        model = models.Spec

    sub = factory.Sequence(lambda n: f"sub {n}")
    id = factory.Sequence(spec_calc_id)
    name = factory.Sequence(lambda n: f"name {n}")
    updated_at = factory.Sequence(spec_calc_updated_at)

    version = factory.Sequence(lambda n: f"version {n}")
    title = factory.Sequence(lambda n: f"title {n}")
    description = factory.Sequence(lambda n: f"description {n}")
    model_count = factory.Sequence(lambda n: (n + 1) * 10 + 2)

    updated_at_id = factory.Sequence(
        lambda n: models.Spec.calc_index_values(
            updated_at=spec_calc_updated_at(n),
            id_=spec_calc_id(n),
        ).updated_at_id
    )
    id_updated_at = factory.Sequence(
        lambda n: models.Spec.calc_index_values(
            updated_at=spec_calc_updated_at(n),
            id_=spec_calc_id(n),
        ).id_updated_at
    )


class CredentialsFactory(factory.Factory):
    """Factory for Credentials model."""

    class Meta:
        """Meta class."""

        model = models.Credentials

    sub = factory.Sequence(lambda n: f"sub {n}")
    id = factory.Sequence(lambda n: f"credentials id {n}")

    public_key = factory.Sequence(lambda n: f"public key {n}")
    secret_key_hash = factory.Sequence(lambda n: f"secret key hash {n}".encode())
    salt = factory.Sequence(lambda n: f"salt {n}".encode())

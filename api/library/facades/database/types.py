"""Types for the database facade."""

import typing

TSub = str
TSpecId = str
TVersion = str
TUpdatedAt = str
TModelCount = int


class TDatabase(typing.Protocol):
    """Interface for database."""

    @staticmethod
    def count_customer_models(*, sub: TSub) -> int:
        """
        Count the number of models a customer has stored.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            The number of models the customer has stored.

        """
        ...

    @staticmethod
    def create_update_spec(
        *, sub: TSub, spec_id: TSpecId, version: TVersion, model_count: TModelCount
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.
            version: The version of the spec.
            model_count: The number of models in the spec.

        """
        ...

    @staticmethod
    def get_latest_spec_version(*, sub: TSub, spec_id: TSpecId) -> TVersion:
        """
        Get the latest version for a spec.

        Raises NotFoundError if the spec is not found in the database.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        Returns:
            The latest version of the spec.

        """
        ...

    @staticmethod
    def list_specs(*, sub: TSub) -> typing.List[TSpecId]:
        """
        List all available specs for a customer.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of all spec id for the customer.

        """
        ...

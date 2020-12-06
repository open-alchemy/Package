"""DynamoDB implementation of the database facade."""

import typing

from . import models, types


class Database:
    """Interface for DynamoDB database."""

    @staticmethod
    def count_customer_models(*, sub: types.TSub) -> int:
        """
        Count the number of models a customer has stored.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            The number of models the customer has stored.

        """
        return models.PackageStorage.count_customer_models(sub=sub)

    @staticmethod
    def create_update_spec(
        *,
        sub: types.TSub,
        spec_id: types.TSpecId,
        version: types.TVersion,
        model_count: types.TModelCount
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.
            version: types.The version of the spec.
            model_count: types.The number of models in the spec.

        """
        models.PackageStorage.create_update_item(
            sub=sub, spec_id=spec_id, version=version, model_count=model_count
        )

    @staticmethod
    def get_latest_spec_version(
        *, sub: types.TSub, spec_id: types.TSpecId
    ) -> types.TVersion:
        """
        Get the latest version for a spec.

        Raises NotFoundError if the spec is not found in the database.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        Returns:
            The latest version of the spec.

        """
        return models.PackageStorage.get_latest_spec_version(sub=sub, spec_id=spec_id)

    @staticmethod
    def list_specs(*, sub: types.TSub) -> typing.List[types.TSpecId]:
        """
        List all available specs for a customer.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of all spec id for the customer.

        """
        return models.PackageStorage.list_specs(sub=sub)

    @staticmethod
    def delete_spec(*, sub: types.TSub, spec_id: types.TSpecId) -> None:
        """
        Delete a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        """
        models.PackageStorage.delete_spec(sub=sub, spec_id=spec_id)

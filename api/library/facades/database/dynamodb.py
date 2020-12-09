"""DynamoDB implementation of the database facade."""

import typing

from . import models, types, exceptions


class Database:
    """Interface for DynamoDB database."""

    FREE_TIER_MODEL_COUNT = 100

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

    @classmethod
    def check_would_exceed_free_tier(
        cls, *, sub: types.TSub, model_count: types.TModelCount
    ) -> types.TCheckWouldExceedFreeTierReturn:
        """
        Check whether adding model_count additional models would exceed the free tier.

        Args:
            sub: Unique identifier for a cutsomer.
            model_count: The number of models that would be added.

        Returns:
            Whether the free tier would be exceeded and a reason if so.

        """
        current_count = cls.count_customer_models(sub=sub)
        if current_count + model_count > cls.FREE_TIER_MODEL_COUNT:
            return types.TCheckWouldExceedFreeTierReturn(
                result=True,
                reason="with this spec the maximum number of "
                f"{cls.FREE_TIER_MODEL_COUNT} models for the free "
                f"tier would be exceeded, current models count: {current_count}, "
                f"models in this spec: {model_count}",
            )

        return types.TCheckWouldExceedFreeTierReturn(result=False, reason=None)

    @staticmethod
    def create_update_spec(
        *,
        sub: types.TSub,
        spec_id: types.TSpecId,
        version: types.TVersion,
        model_count: types.TModelCount,
        title: types.TOptTitle = None,
        description: types.TDescription = None,
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.
            version: types.The version of the spec.
            model_count: types.The number of models in the spec.
            title: The title of a spec.
            description: The description of a spec.

        """
        models.PackageStorage.create_update_item(
            sub=sub,
            spec_id=spec_id,
            version=version,
            model_count=model_count,
            title=title,
            description=description,
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
    def list_specs(*, sub: types.TSub) -> types.TSpecInfoList:
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

    @staticmethod
    def list_spec_versions(
        *, sub: types.TSub, spec_id: types.TSpecId
    ) -> types.TSpecInfoList:
        """
        List all available versions for a spec for a customer.

        Filters for a customer and for updated_at_spec_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        Returns:
            List of information for all versions of a spec for the customer.

        """
        spec_infos = models.PackageStorage.list_spec_versions(sub=sub, spec_id=spec_id)
        if not spec_infos:
            raise exceptions.NotFoundError(f"could not find spec id {spec_id}")
        return spec_infos

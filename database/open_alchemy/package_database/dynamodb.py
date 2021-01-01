"""DynamoDB implementation of the database facade."""

from . import config, exceptions, models, types


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
        return models.Spec.count_customer_models(sub=sub)

    @classmethod
    def check_would_exceed_free_tier(
        cls, *, sub: types.TSub, model_count: types.TSpecModelCount
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
        if current_count + model_count > config.get().free_tier_model_count:
            return types.TCheckWouldExceedFreeTierReturn(
                result=True,
                reason="with this spec the maximum number of "
                f"{config.get().free_tier_model_count} models for the free "
                f"tier would be exceeded, current models count: {current_count}, "
                f"models in this spec: {model_count}",
            )

        return types.TCheckWouldExceedFreeTierReturn(result=False, reason=None)

    @staticmethod
    def create_update_spec(
        *,
        sub: types.TSub,
        id_: types.TSpecId,
        version: types.TSpecVersion,
        model_count: types.TSpecModelCount,
        title: types.TOptSpecTitle = None,
        description: types.TOptSpecDescription = None,
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.
            version: types.The version of the spec.
            model_count: types.The number of models in the spec.
            title: The title of a spec.
            description: The description of a spec.

        """
        models.Spec.create_update_item(
            sub=sub,
            id_=id_,
            version=version,
            model_count=model_count,
            title=title,
            description=description,
        )

    @staticmethod
    def get_latest_spec_version(
        *, sub: types.TSub, id_: types.TSpecId
    ) -> types.TSpecVersion:
        """
        Get the latest version for a spec.

        Raises NotFoundError if the spec is not found in the database.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.

        Returns:
            The latest version of the spec.

        """
        return models.Spec.get_latest_spec_version(sub=sub, id_=id_)

    @staticmethod
    def list_specs(*, sub: types.TSub) -> types.TSpecInfoList:
        """
        List all available specs for a customer.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of all spec id for the customer.

        """
        return models.Spec.list_specs(sub=sub)

    @staticmethod
    def delete_spec(*, sub: types.TSub, id_: types.TSpecId) -> None:
        """
        Delete a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.

        """
        models.Spec.delete_spec(sub=sub, id_=id_)

    @staticmethod
    def list_spec_versions(
        *, sub: types.TSub, id_: types.TSpecId
    ) -> types.TSpecInfoList:
        """
        List all available versions for a spec for a customer.

        Filters for a customer and for updated_at_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.
            id: Unique identifier for the spec for a package.

        Returns:
            List of information for all versions of a spec for the customer.

        """
        spec_infos = models.Spec.list_spec_versions(sub=sub, id_=id_)
        if not spec_infos:
            raise exceptions.NotFoundError(f"could not find spec id {id_}")
        return spec_infos

"""Types for the database facade."""

import typing

from ... import types

TSub = types.TUser
TSpecId = types.TSpecId
TVersion = types.TSpecVersion
TTitle = types.TSpecTitle
TOptTitle = types.TSpecOptTitle
TDescription = types.TSpecDescription
TOptDescription = types.TSpecOptDescription
TUpdatedAt = str
TModelCount = types.TSpecModelCount


class _TSpecInfoBase(typing.TypedDict, total=False):
    """Optional information about a spec."""

    title: TTitle
    descritpion: TDescription


class TSpecInfo(_TSpecInfoBase, total=True):
    """All information about a spec."""

    spec_id: TSpecId
    version: TVersion
    updated_at: int


TSpecInfoList = typing.List[TSpecInfo]


class TCheckWouldExceedFreeTierReturn(typing.NamedTuple):
    """The return value of the free tier check."""

    # Whether the free tier would be exceeded
    result: bool
    # If the result is True, the reason that it would be
    reason: typing.Optional[str]


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
    def check_would_exceed_free_tier(
        *, sub: TSub, model_count: TModelCount
    ) -> TCheckWouldExceedFreeTierReturn:
        """
        Check whether adding model_count additional models would exceed the free tier.

        Args:
            sub: Unique identifier for a cutsomer.
            model_count: The number of models that would be added.

        Returns:
            Whether the free tier would be exceeded and a reason if so.

        """
        ...

    @staticmethod
    def create_update_spec(
        *,
        sub: TSub,
        spec_id: TSpecId,
        version: TVersion,
        model_count: TModelCount,
        title: TOptTitle = None,
        description: TDescription = None
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.
            version: The version of the spec.
            model_count: The number of models in the spec.
            title: The title of a spec.
            description: The description of a spec.

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
    def list_specs(*, sub: TSub) -> TSpecInfoList:
        """
        List all available specs for a customer.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of all spec id for the customer.

        """
        ...

    @staticmethod
    def delete_spec(*, sub: TSub, spec_id: TSpecId) -> None:
        """
        Delete a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        """
        ...

    @staticmethod
    def list_spec_versions(*, sub: TSub, spec_id: TSpecId) -> TSpecInfoList:
        """
        List all available versions for a spec for a customer.

        Filters for a customer and for updated_at_spec_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.
            spec_id: Unique identifier for the spec for a package.

        Returns:
            List of information for all versions of a spec for the customer.

        """
        ...

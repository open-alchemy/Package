"""Types for the database facade."""

import dataclasses
import typing

TSub = str

TSpecId = str
TSpecName = str
TSpecVersion = str
TSpecTitle = str
TOptSpecTitle = typing.Optional[TSpecTitle]
TSpecDescription = str
TOptSpecDescription = typing.Optional[TSpecDescription]
TSpecUpdatedAt = str
TSpecModelCount = int

TCredentialsId = str
TCredentialsPublicKey = str
TCredentialsSecretKeyHash = bytes
TCredentialsSalt = bytes


class _TSpecInfoBase(typing.TypedDict, total=False):
    """Optional information about a spec."""

    title: TSpecTitle
    description: TSpecDescription


class TSpecInfo(_TSpecInfoBase, total=True):
    """
    All information about a spec.

    Attrs:
        id: Unique identifier for the spec
        version: The version of the spec
        updated_at: The last time the spec was updated
        model_count: The number of models in the spec

    """

    id: TSpecId
    name: TSpecName
    version: TSpecVersion
    updated_at: int
    model_count: TSpecModelCount


TSpecInfoList = typing.List[TSpecInfo]


class TCredentialsInfo(typing.TypedDict, total=True):
    """
    All information about particular credentials.

    Attrs:
        id: Unique identifier for the credentials.
        public_key: Public identifier for the credentials.
        salt: Random value used to generate the credentials.

    """

    id: TCredentialsId
    public_key: TCredentialsPublicKey
    salt: TCredentialsSalt


TCredentialsInfoList = typing.List[TCredentialsInfo]


@dataclasses.dataclass
class CredentialsAuthInfo:
    """
    Information about a credential needed for authentication.

    Attrs:
        sub: Unique identifier for a cutsomer.
        secret_key_hash: Value derived from the secret key that is safe to store.
        salt: Random value used to generate the credentials.

    """

    sub: TSub
    secret_key_hash: TCredentialsSecretKeyHash
    salt: TCredentialsSalt


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
        *,
        sub: TSub,
        name: TSpecName,
        version: TSpecVersion,
        model_count: TSpecModelCount,
        title: TOptSpecTitle = None,
        description: TSpecDescription = None
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            name: The display name of the spec.
            version: The version of the spec.
            model_count: The number of models in the spec.
            title: The title of a spec.
            description: The description of a spec.

        """
        ...

    @staticmethod
    def get_latest_spec_version(*, sub: TSub, name: TSpecName) -> TSpecVersion:
        """
        Get the latest version for a spec.

        Raises NotFoundError if the spec is not found in the database.

        Args:
            sub: Unique identifier for a cutsomer.
            name: The display name of the spec.

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
    def get_spec(*, sub: TSub, name: TSpecName) -> typing.Optional[TSpecInfo]:
        """
        Retrieve a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            name: The display name of the spec.

        Returns:
            Information about the spec

        """
        ...

    @staticmethod
    def delete_spec(*, sub: TSub, name: TSpecName) -> None:
        """
        Delete a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            name: The display name of the spec.

        """
        ...

    @staticmethod
    def list_spec_versions(*, sub: TSub, name: TSpecName) -> TSpecInfoList:
        """
        List all available versions for a spec for a customer.

        Filters for a customer and for updated_at_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.
            name: The display name of the spec.

        Returns:
            List of information for all versions of a spec for the customer.

        """
        ...

    @staticmethod
    def delete_all_specs(*, sub: TSub) -> None:
        """
        Delete all the specs for a user.

        Args:
            sub: Unique identifier for a cutsomer.

        """
        ...

    @staticmethod
    def list_credentials(*, sub: TSub) -> TCredentialsInfoList:
        """
        List all available credentials for a user.

        Filters for a customer and returns all credentials.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of information for all credentials of the customer.

        """
        ...

    @staticmethod
    def create_update_credentials(
        *,
        sub: TSub,
        id_: TCredentialsId,
        public_key: TCredentialsPublicKey,
        secret_key_hash: TCredentialsSecretKeyHash,
        salt: TCredentialsSalt
    ) -> None:
        """
        Create or update a spec.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the credentials.
            public_key: Public identifier for the credentials.
            secret_key_hash: Value derived from the secret key that is safe to store.
            salt: Random value used to generate the credentials.

        """
        ...

    @staticmethod
    def get_credentials(
        *, sub: TSub, id_: TCredentialsId
    ) -> typing.Optional[TCredentialsInfo]:
        """
        Retrieve credentials.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the credentials.

        Returns:
            Information about the credentials.

        """
        ...

    @staticmethod
    def get_user(
        *, public_key: TCredentialsPublicKey
    ) -> typing.Optional[CredentialsAuthInfo]:
        """
        Retrieve a user and information to authenticate the user.

        Args:
            public_key: Public identifier for the credentials.

        Returns:
            Information needed to authenticate the user.

        """
        ...

    @staticmethod
    def delete_credentials(*, sub: TSub, id_: TCredentialsId) -> None:
        """
        Delete the credentials.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the credentials.

        """
        ...

    @staticmethod
    def delete_all_credentials(*, sub: TSub) -> None:
        """
        Delete all the credentials for a user.

        Args:
            sub: Unique identifier for a cutsomer.

        """
        ...

    @classmethod
    def delete_all(cls, *, sub: TSub) -> None:
        """
        Delete all the items for a user.

        Args:
            sub: Unique identifier for a cutsomer.

        """
        ...

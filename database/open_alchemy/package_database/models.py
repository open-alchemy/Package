"""Database models."""

import time
import typing

from pynamodb import attributes, indexes, models

from . import config, exceptions, types

TSpecUpdatedAtSpecId = str
TSpecSpecIdUpdatedAt = str


class TSpecIndexValues(typing.NamedTuple):
    """The index values for Spec."""

    updated_at_id: TSpecUpdatedAtSpecId
    id_updated_at: TSpecSpecIdUpdatedAt


class SpecIdUpdatedAtIndex(indexes.LocalSecondaryIndex):
    """Local secondary index for querying based on id."""

    class Meta:
        """Meta class."""

        projection = indexes.AllProjection()
        index_name = config.get().specs_local_secondary_index_name

        if config.get().stage == config.Stage.TEST:
            host = "http://localhost:8000"

    sub = attributes.UnicodeAttribute(hash_key=True)
    id_updated_at = attributes.UnicodeAttribute(range_key=True)


class Spec(models.Model):
    """
    Information about a spec.

    Attrs:
        UPDATED_AT_LATEST: Constant for what to set updated_at to to indicate it is the
            latest record

        sub: Unique identifier for a customer
        id: Unique identifier for a spec for a package
        updated_at: The last time the spec version was updated in integer seconds since
            epoch stored as a string or 'latest' for the copy of the latest version of
            the spec.

        version: The version of a spec for a package
        title: The title of a spec
        description: The description of a spec
        model_count: The number of 'x-tablename' and 'x-inherits' in a spec

        updated_at_id: Combination of 'updated_at' and 'id' separeted with #
        id_updated_at: Combination of 'id' and 'updated_at' separeted with #

        id_updated_at_index: Index for querying id_updated_at efficiently

    """

    UPDATED_AT_LATEST = "latest"

    class Meta:
        """Meta class."""

        table_name = config.get().specs_table_name

        if config.get().stage == config.Stage.TEST:
            host = "http://localhost:8000"

    sub = attributes.UnicodeAttribute(hash_key=True)
    id = attributes.UnicodeAttribute()
    updated_at = attributes.UnicodeAttribute()

    version = attributes.UnicodeAttribute()
    title = attributes.UnicodeAttribute(null=True)
    description = attributes.UnicodeAttribute(null=True)
    model_count = attributes.NumberAttribute()

    updated_at_id = attributes.UnicodeAttribute(range_key=True)
    id_updated_at = attributes.UnicodeAttribute()

    id_updated_at_index = SpecIdUpdatedAtIndex()

    @classmethod
    def count_customer_models(cls, *, sub: types.TSub) -> int:
        """
        Count the number of models on the latest specs for a customer.

        Filters for a particular customer and updated_at_id to start with
        'latest#' and sums over model_count.

        Args:
            sub: Unique identifier for the customer.

        Returns:
            The sum of the model count on the latest version of each unique spec for
            the customer.

        """
        return sum(
            map(
                lambda item: int(item.model_count),
                cls.query(
                    sub,
                    cls.updated_at_id.startswith(f"{cls.UPDATED_AT_LATEST}#"),
                ),
            )
        )

    @classmethod
    def calc_index_values(
        cls, *, updated_at: types.TSpecUpdatedAt, id_: types.TSpecId
    ) -> TSpecIndexValues:
        """
        Calculate the updated_at_id value.

        Args:
            updated_at: The value for updated_at
            id_: The value for id

        Returns:
            The value for updated_at_id

        """
        # Zero pad updated_at if it is not latest
        if updated_at != cls.UPDATED_AT_LATEST:
            updated_at = updated_at.zfill(20)

        return TSpecIndexValues(
            updated_at_id=f"{updated_at}#{id_}",
            id_updated_at=f"{id_}#{updated_at}",
        )

    @classmethod
    def create_update_item(
        cls,
        *,
        sub: types.TSub,
        id_: types.TSpecId,
        version: types.TSpecVersion,
        model_count: types.TSpecModelCount,
        title: types.TSpecTitle = None,
        description: types.TSpecDescription = None,
    ) -> None:
        """
        Create or update an item.

        Creates or updates 2 items in the database. The updated_at attribute for the
        first is calculated based on seconds since epoch and for the second is set to
        'latest'. Also computes the sort key updated_at_id based on updated_at and
        id.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.
            version: The version of the spec.
            model_count: The number of models in the spec.
            title: The title of a spec
            description: The description of a spec

        """
        # Write item
        updated_at = str(int(time.time()))
        index_values = cls.calc_index_values(updated_at=updated_at, id_=id_)
        item = cls(
            sub=sub,
            id=id_,
            updated_at=updated_at,
            version=version,
            title=title,
            description=description,
            model_count=model_count,
            updated_at_id=index_values.updated_at_id,
            id_updated_at=index_values.id_updated_at,
        )
        item.save()

        # Write latest item
        updated_at_latest = cls.UPDATED_AT_LATEST
        index_values_latest = cls.calc_index_values(
            updated_at=updated_at_latest, id_=id_
        )
        item_latest = cls(
            sub=sub,
            id=id_,
            version=version,
            updated_at=updated_at,
            title=title,
            description=description,
            model_count=model_count,
            updated_at_id=index_values_latest.updated_at_id,
            id_updated_at=index_values_latest.id_updated_at,
        )
        item_latest.save()

    @classmethod
    def get_latest_spec_version(
        cls, *, sub: types.TSub, id_: types.TSpecId
    ) -> types.TSpecVersion:
        """
        Get the latest version for a spec.

        Raises NotFoundError if the spec is not found in the database.

        Calculates updated_at_id by setting updated_at to latest and using the
        id. Tries to retrieve an item for a customer based on the sort key.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.

        Returns:
            The latest version of the spec.

        """
        try:
            item = cls.get(
                hash_key=sub,
                range_key=cls.calc_index_values(
                    updated_at=cls.UPDATED_AT_LATEST, id_=id_
                ).updated_at_id,
            )
            return item.version
        except cls.DoesNotExist as exc:
            raise exceptions.NotFoundError(
                f"the spec {id_} does not exist for customer {sub}"
            ) from exc

    @staticmethod
    def item_to_info(item: "Spec") -> types.TSpecInfo:
        """Convert item to dict with information about the spec."""
        info: types.TSpecInfo = {
            "id": item.id,
            "updated_at": int(item.updated_at),
            "version": item.version,
            "model_count": int(item.model_count),
        }
        if item.title is not None:
            info["title"] = item.title
        if item.description is not None:
            info["description"] = item.description
        return info

    @classmethod
    def list_specs(cls, *, sub: types.TSub) -> types.TSpecInfoList:
        """
        List all available specs for a customer.

        Filters for a customer and for updated_at_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of information for all specs for the customer.

        """
        return list(
            map(
                cls.item_to_info,
                cls.query(
                    sub,
                    cls.updated_at_id.startswith(f"{cls.UPDATED_AT_LATEST}#"),
                ),
            )
        )

    @classmethod
    def delete_spec(cls, *, sub: types.TSub, id_: types.TSpecId) -> None:
        """
        Delete a spec from the database.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.

        """
        items = cls.id_updated_at_index.query(
            sub, cls.id_updated_at.startswith(f"{id_}#")
        )
        with cls.batch_write() as batch:
            for item in items:
                batch.delete(item)

    @classmethod
    def list_spec_versions(
        cls, *, sub: types.TSub, id_: types.TSpecId
    ) -> types.TSpecInfoList:
        """
        List all available versions for a spec for a customer.

        Filters for a customer and for updated_at_id to start with latest.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the spec for a package.

        Returns:
            List of information for all versions of a spec for the customer.

        """
        items = cls.id_updated_at_index.query(
            sub,
            cls.id_updated_at.startswith(f"{id_}#"),
        )
        items_no_latest = filter(
            lambda item: not item.updated_at_id.startswith(f"{cls.UPDATED_AT_LATEST}#"),
            items,
        )
        return list(map(cls.item_to_info, items_no_latest))


class PublicKeyIndex(indexes.GlobalSecondaryIndex):
    """Global secondary index for querying based on the public key."""

    class Meta:
        """Meta class."""

        projection = indexes.AllProjection()
        index_name = config.get().credentials_global_secondary_index_name

        if config.get().stage == config.Stage.TEST:
            host = "http://localhost:8000"
            read_capacity_units = 1
            write_capacity_units = 1

    public_key = attributes.UnicodeAttribute(hash_key=True)


class Credentials(models.Model):
    """
    Information about credentials.

    Attrs:
        sub: Unique identifier for a customer
        id: Unique identifier for particular credentials

        public_key: Public identifier for the credentials.
        secret_key_hash: Value derived from the secret key that is safe to store.
        salt: Random value used to generate the credentials.

    """

    class Meta:
        """Meta class."""

        table_name = config.get().credentials_table_name

        if config.get().stage == config.Stage.TEST:
            host = "http://localhost:8000"

    sub = attributes.UnicodeAttribute(hash_key=True)
    id = attributes.UnicodeAttribute(range_key=True)

    public_key = attributes.UnicodeAttribute()
    secret_key_hash = attributes.BinaryAttribute()
    salt = attributes.BinaryAttribute()

    public_key_index = PublicKeyIndex()

    @staticmethod
    def item_to_info(item: "Credentials") -> types.TCredentialsInfo:
        """Convert item to dict with information about the credentials."""
        info: types.TCredentialsInfo = {
            "id": item.id,
            "public_key": item.public_key,
            "salt": item.salt,
        }
        return info

    @classmethod
    def list_credentials(cls, *, sub: types.TSub) -> types.TCredentialsInfoList:
        """
        List all available credentials for a user.

        Filters for a customer and returns all credentials.

        Args:
            sub: Unique identifier for a cutsomer.

        Returns:
            List of information for all credentials of the customer.

        """
        return list(map(cls.item_to_info, cls.query(sub)))

    @classmethod
    def create_update_item(
        cls,
        *,
        sub: types.TSub,
        id_: types.TCredentialsId,
        public_key: types.TCredentialsPublicKey,
        secret_key_hash: types.TCredentialsSecretKeyHash,
        salt: types.TCredentialsSalt,
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
        item = cls(
            sub=sub,
            id=id_,
            public_key=public_key,
            secret_key_hash=secret_key_hash,
            salt=salt,
        )
        item.save()

    @classmethod
    def get_credentials(
        cls, *, sub: types.TSub, id_: types.TCredentialsId
    ) -> typing.Optional[types.TCredentialsInfo]:
        """
        Retrieve credentials.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the credentials.

        Returns:
            Information about the credentials.

        """
        try:
            item = cls.get(hash_key=sub, range_key=id_)
        except cls.DoesNotExist:
            return None

        return cls.item_to_info(item)

    @classmethod
    def get_user(
        cls, *, public_key: types.TCredentialsPublicKey
    ) -> typing.Optional[types.CredentialsAuthInfo]:
        """
        Retrieve a user and information to authenticate the user.

        Args:
            public_key: Public identifier for the credentials.

        Returns:
            Information needed to authenticate the user.

        """
        item = next(cls.public_key_index.query(hash_key=public_key), None)

        if item is None:
            return None

        return types.CredentialsAuthInfo(
            sub=item.sub, secret_key_hash=item.secret_key_hash, salt=item.salt
        )

    @classmethod
    def delete_credentials(cls, *, sub: types.TSub, id_: types.TCredentialsId) -> None:
        """
        Delete the credentials.

        Args:
            sub: Unique identifier for a cutsomer.
            id_: Unique identifier for the credentials.

        """
        try:
            item = cls.get(hash_key=sub, range_key=id_)
            item.delete()
        except cls.DoesNotExist:
            pass

    @classmethod
    def delete_all_credentials(cls, *, sub: types.TSub) -> None:
        """
        Delete all the credentials for a user.

        Args:
            sub: Unique identifier for a cutsomer.

        """
        items = cls.query(hash_key=sub)
        with cls.batch_write() as batch:
            for item in items:
                batch.delete(item)

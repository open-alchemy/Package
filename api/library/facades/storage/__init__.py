"""Storage facade."""

import typing

from ... import config
from ... import types as library_types
from . import exceptions, memory, s3, types


def _construct_storage() -> types.TStorage:
    """Construct the storage facade."""
    config_instance = config.get()

    if config_instance.stage == config.Stage.TEST:
        return memory.Storage()

    if config_instance.stage == config.Stage.PROD:
        return s3.Storage(config_instance.package_storage_bucket_name)

    raise AssertionError(f"unsupported stage {config_instance.stage}")


class TCache(typing.TypedDict, total=True):
    """Cache for storage."""

    storage: typing.Optional[types.TStorage]


_CACHE: TCache = {"storage": None}


def get_storage() -> types.TStorage:
    """Return a facade for the storage."""
    if _CACHE["storage"] is None:
        _CACHE["storage"] = _construct_storage()
    assert _CACHE["storage"] is not None
    return _CACHE["storage"]


class _StorageFacade:
    """Facade for the storage that exposes important functionality."""

    @staticmethod
    def create_update_spec(
        user: library_types.TUser,
        spec_id: library_types.TSpecId,
        version: library_types.TSpecVersion,
        spec_str: library_types.TSpecValue,
    ) -> None:
        """
        Create or update a spec.

        Args:
            user: The user that owns the spec.
            spec_id: Unique identifier for the spec.
            version: The version of the spec.
            spec_str: The value of the spec.

        """
        get_storage().set(
            key=f"{user}/{spec_id}/{version}-spec.json",
            value=spec_str,
        )

    @staticmethod
    def get_spec(
        user: library_types.TUser,
        spec_id: library_types.TSpecId,
        version: library_types.TSpecVersion,
    ) -> library_types.TSpecValue:
        """
        Create or update a spec.

        Args:
            user: The user that owns the spec.
            spec_id: Unique identifier for the spec.
            version: The version of the spec.

        """
        return get_storage().get(key=f"{user}/{spec_id}/{version}-spec.json")

    @staticmethod
    def delete_spec(
        user: library_types.TUser,
        spec_id: library_types.TSpecId,
    ) -> None:
        """
        Delete a spec.

        Args:
            user: The user that owns the spec.
            spec_id: Unique identifier for the spec.

        """
        delete_keys = get_storage().list(prefix=f"{user}/{spec_id}")
        if not delete_keys:
            raise exceptions.StorageError("no keys to delete")
        get_storage().delete_all(keys=delete_keys)

    @staticmethod
    def get_spec_versions(
        user: library_types.TUser, spec_id: library_types.TSpecId
    ) -> library_types.TSpecVersions:
        """
        Get the available versions for a spec.

        Raises ObjectNotFoundError if the spec does not exist.

        Args:
            user: The user that owns the spec.
            spec_id: Unique identifier for the spec.

        Returns:
            All available versions of the spec.

        """
        prefix = f"{user}/{spec_id}/"
        suffix = "-spec.json"
        keys = get_storage().list(prefix=prefix, suffix=suffix)

        if not keys:
            raise exceptions.ObjectNotFoundError(
                f"the spec with id {spec_id} was not found"
            )

        return list(map(lambda key: key[len(prefix) : -len(suffix)], keys))


_FACADE = _StorageFacade()


def get_storage_facade() -> _StorageFacade:
    """Return a facade for the storage."""
    return _FACADE

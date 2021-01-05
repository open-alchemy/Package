"""Storage facade."""

import typing

from packaging import utils

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
    def cal_id(name: library_types.TSpecName) -> library_types.TSpecId:
        """Calculate the id of a spec."""
        return utils.canonicalize_name(name)

    @classmethod
    def create_update_spec(
        cls,
        *,
        user: library_types.TUser,
        name: library_types.TSpecName,
        version: library_types.TSpecVersion,
        spec_str: library_types.TSpecValue,
    ) -> None:
        """
        Create or update a spec.

        Args:
            user: The user that owns the spec.
            name: The display name of the spec.
            version: The version of the spec.
            spec_str: The value of the spec.

        """
        id_ = cls.cal_id(name)
        get_storage().set(
            key=f"{user}/{id_}/{version}-spec.json",
            value=spec_str,
        )

    @classmethod
    def get_spec(
        cls,
        *,
        user: library_types.TUser,
        name: library_types.TSpecName,
        version: library_types.TSpecVersion,
    ) -> library_types.TSpecValue:
        """
        Create or update a spec.

        Args:
            user: The user that owns the spec.
            name: The display name of the spec.
            version: The version of the spec.

        """
        id_ = cls.cal_id(name)
        return get_storage().get(key=f"{user}/{id_}/{version}-spec.json")

    @classmethod
    def delete_spec(
        cls,
        *,
        user: library_types.TUser,
        name: library_types.TSpecName,
    ) -> None:
        """
        Delete a spec.

        Args:
            user: The user that owns the spec.
            name: The display name of the spec.

        """
        id_ = cls.cal_id(name)
        delete_keys = get_storage().list(prefix=f"{user}/{id_}")
        if not delete_keys:
            raise exceptions.StorageError("no keys to delete")
        get_storage().delete_all(keys=delete_keys)

    @classmethod
    def get_spec_versions(
        cls, *, user: library_types.TUser, name: library_types.TSpecName
    ) -> library_types.TSpecVersions:
        """
        Get the available versions for a spec.

        Raises ObjectNotFoundError if the spec does not exist.

        Args:
            user: The user that owns the spec.
            name: The display name of the spec.

        Returns:
            All available versions of the spec.

        """
        id_ = cls.cal_id(name)
        prefix = f"{user}/{id_}/"
        suffix = "-spec.json"
        keys = get_storage().list(prefix=prefix, suffix=suffix)

        if not keys:
            raise exceptions.ObjectNotFoundError(
                f"the spec with {id_=}, {name=} was not found"
            )

        return list(map(lambda key: key[len(prefix) : -len(suffix)], keys))


_FACADE = _StorageFacade()


def get_storage_facade() -> _StorageFacade:
    """Return a facade for the storage."""
    return _FACADE

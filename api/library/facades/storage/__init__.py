"""Storage facade."""

from . import exceptions
from . import memory
from . import s3
from . import types
from ... import types as library_types
from ... import config


def _construct_storage() -> types.TStorage:
    """Construct the storage facade."""
    environment = config.get_env()

    if environment.stage == config.Stage.TEST:
        return memory.Storage()

    if environment.stage == config.Stage.PROD:
        return s3.Storage(environment.package_storage_bucket_name)

    raise AssertionError(f"unsupported stage {environment.stage}")


_STORAGE = _construct_storage()


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
        _STORAGE.set(
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
        return _STORAGE.get(key=f"{user}/{spec_id}/{version}-spec.json")

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
        delete_keys = _STORAGE.list(prefix=f"{user}/{spec_id}")
        if not delete_keys:
            raise exceptions.StorageError("no keys to delete")
        _STORAGE.delete_all(keys=delete_keys)


_FACADE = _StorageFacade()


def get_storage() -> _StorageFacade:
    """Return a facade for the storage."""
    return _FACADE

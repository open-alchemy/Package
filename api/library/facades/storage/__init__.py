"""Storage facade."""

from . import exceptions
from . import memory
from . import s3
from . import types
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


def get_storage() -> types.TStorage:
    """Return a facade for the storage."""
    return _STORAGE

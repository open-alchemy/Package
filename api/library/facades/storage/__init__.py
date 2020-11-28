"""Storage facade."""

from . import exceptions
from . import memory
from . import types


def _construct_storage() -> types.TStorage:
    """Construct the storage facade."""
    return memory.Storage()


_STORAGE = _construct_storage()


def get_storage() -> types.TStorage:
    """Return a facade for the seed."""
    return _STORAGE

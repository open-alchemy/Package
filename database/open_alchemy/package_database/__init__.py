"""Package database facade."""

from . import dynamodb, exceptions, types


def _construct() -> types.TDatabase:
    """Construct the database facade."""
    return dynamodb.Database()


_DATABASE = _construct()


def get() -> types.TDatabase:
    """Return a facade for the database."""
    return _DATABASE

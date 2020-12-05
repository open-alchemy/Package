"""Database facade."""

from . import dynamodb
from . import types


def _construct_database() -> types.TDatabase:
    """Construct the database facade."""
    return dynamodb.Database()


_DATABASE = _construct_database()


def get_database() -> types.TDatabase:
    """Return a facade for the database."""
    return _DATABASE

"""Database exceptions."""

from ... import exceptions


class DatabaseError(exceptions.BaseError):
    """The base exceptions for databases."""


class NotFoundError(DatabaseError):
    """When an item was not found in the database."""

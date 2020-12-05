"""Database exceptions."""

from ... import exceptions


class BaseError(exceptions.BaseError):
    """The base exceptions for databases."""


class NotFoundError(BaseError):
    """When an item was not found in the database."""

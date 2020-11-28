"""Errors for the storage facade."""

from ... import exceptions


class StorageError(exceptions.BaseError):
    """Base exception for storage errors."""


class ObjectNotFoundError(StorageError):
    """Raised when an object cannot be found."""

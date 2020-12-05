"""Exceptions that can be raised."""


class BaseError(Exception):
    """The base exception."""


class LoadSpecError(BaseError):
    """Raised when a spec cannot be loaded from a string or it is malformed."""

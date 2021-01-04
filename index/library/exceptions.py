"""Exceptions for index."""


class BaseError(Exception):
    """All errors derrive from this error."""


class UnauthorizedError(BaseError):
    """Raised when a user is unauthorized."""

"""Shared types."""

import dataclasses
import enum

TAuthorizationValue = str
TUri = str


@dataclasses.dataclass
class TAuthorization:
    """Authorization information."""

    public_key: str
    secret_key: str


@enum.unique
class TRequestType(str, enum.Enum):
    """
    The type of request.

    Attrs:
        LIST: List the available packages that can be installed.
        INSTALL: Install a particular package.

    """

    LIST = "LIST"
    INSTALL = "INSTALL"

"""Shared types."""

import dataclasses
import enum

from open_alchemy.package_database import types as database_types

TAuthorizationValue = str
TUri = str
CredentialsAuthInfo = database_types.CredentialsAuthInfo
TResponseValue = str


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


@dataclasses.dataclass
class TResponse:
    """
    Information for the response to the request.

    Attrs:
        type: The type of response.
        value: The value to create the response.

    """

    type: TRequestType
    value: TResponseValue

"""Tests for the library."""

import base64

import library
import pytest
from library import exceptions
from open_alchemy.package_database import factory

PARSE_AUTHORIZATION_HEADER_ERROR_TESTS = [
    pytest.param("invalid", id="Bearer missing"),
    pytest.param("Basic invalid", id="Bearer value not base64 encoded"),
    pytest.param("Basic invalid=", id="Bearer value not base64 encoded"),
    pytest.param(
        f"Basic {base64.b64encode('invalid'.encode()).decode()}",
        id="Bearer value base64 encoded colon missing",
    ),
    pytest.param(
        f"Basic {base64.b64encode('::'.encode()).decode()}",
        id="Bearer value base64 encoded multiple colon",
    ),
    pytest.param(
        f"Basic {base64.b64encode(':secret key 1'.encode()).decode()}",
        id="Bearer value base64 encoded public key empty",
    ),
    pytest.param(
        f"Basic {base64.b64encode('public key 1:'.encode()).decode()}",
        id="Bearer value base64 encoded secret key empty",
    ),
]


@pytest.mark.parametrize("value", PARSE_AUTHORIZATION_HEADER_ERROR_TESTS)
def test_parse_authorization_header_error(value):
    """
    GIVEN invalid authorization value
    WHEN parse_authorization_header is called with th value
    THEN UnauthorizedError is raised.
    """
    with pytest.raises(exceptions.UnauthorizedError):
        library.parse_authorization_header(value)


def test_parse_authorization_header():
    """
    GIVEN authorization value
    WHEN parse_authorization_header is called with th value
    THEN the public and secret key are retrieved from the authorization.
    """
    public_key = "public key 1"
    secret_key = "secret key 1"
    value = f"Basic {base64.b64encode(f'{public_key}:{secret_key}'.encode()).decode()}"

    returned_authorization = library.parse_authorization_header(value)

    assert returned_authorization.public_key == public_key
    assert returned_authorization.secret_key == secret_key


def test_get_user_error(_clean_credentials_table):
    """
    GIVEN empty database
    WHEN get_user is called
    THEN UnauthorizedError is raised.
    """
    authorization = library.Authorization(
        public_key="public key 1", secret_key="secret key 1"
    )

    with pytest.raises(exceptions.UnauthorizedError):
        library.get_user(authorization=authorization)


def test_get_user(_clean_credentials_table):
    """
    GIVEN database with credentials
    WHEN get_user is called
    THEN then user is returned.
    """
    credentials = factory.CredentialsFactory()
    credentials.save()
    authorization = library.Authorization(
        public_key=credentials.public_key, secret_key="secret key 1"
    )

    returned_user = library.get_user(authorization=authorization)

    assert returned_user.sub == credentials.sub
    assert returned_user.salt == credentials.salt
    assert returned_user.secret_key_hash == credentials.secret_key_hash

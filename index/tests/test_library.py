"""Tests for the library."""

import base64

import library
import pytest
from library import exceptions
from open_alchemy import package_security
from open_alchemy.package_database import factory, types

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


def test_authorize_user_error():
    """
    GIVEN invalid authorization
    WHEN authorize_user is called
    THEN UnauthorizedError is raised.
    """
    authorization = library.Authorization(
        public_key="public key 1", secret_key="secret key 1"
    )
    auth_info = types.CredentialsAuthInfo(
        sub="sub 1", secret_key_hash=b"invalid", salt=b"salt 1"
    )

    with pytest.raises(exceptions.UnauthorizedError):
        library.authorize_user(authorization=authorization, auth_info=auth_info)


def test_authorize_user():
    """
    GIVEN valid authorization
    WHEN authorize_user is called
    THEN UnauthorizedError is not raised.
    """
    secret_key = "secret key 1"
    salt = b"salt 1"
    secret_key_hash = package_security.calculate_secret_key_hash(
        secret_key=secret_key, salt=salt
    )
    authorization = library.Authorization(
        public_key="public key 1", secret_key=secret_key
    )
    auth_info = types.CredentialsAuthInfo(
        sub="sub 1", secret_key_hash=secret_key_hash, salt=salt
    )

    library.authorize_user(authorization=authorization, auth_info=auth_info)


def test_process_invalid_secret_key_error(_clean_credentials_table):
    """
    GIVEN invalid authorization value
    WHEN process is called
    THEN UnauthorizedError is raised.
    """
    credentials = factory.CredentialsFactory()
    credentials.save()
    token = base64.b64encode(f"{credentials.public_key}:invalid".encode()).decode()
    authorization_value = f"Basic {token}"

    with pytest.raises(exceptions.UnauthorizedError):
        library.process(_uri="", authorization_value=authorization_value)


def test_process(_clean_credentials_table):
    """
    GIVEN valid authorization value
    WHEN process is called
    THEN UnauthorizedError is not raised.
    """
    secret_key = "secret key 1"
    salt = b"salt 1"
    secret_key_hash = package_security.calculate_secret_key_hash(
        secret_key=secret_key, salt=salt
    )
    credentials = factory.CredentialsFactory(secret_key_hash=secret_key_hash, salt=salt)
    credentials.save()
    token = base64.b64encode(f"{credentials.public_key}:{secret_key}".encode()).decode()
    authorization_value = f"Basic {token}"

    library.process(_uri="", authorization_value=authorization_value)

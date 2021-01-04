"""Tests for the library."""

import base64

import library
import pytest
from library import exceptions

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

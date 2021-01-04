"""Tests for the library."""

import base64
import time
from unittest import mock

import library
import pytest
from library import exceptions, types
from open_alchemy import package_database, package_security
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
    authorization = types.TAuthorization(
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
    authorization = types.TAuthorization(
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
    authorization = types.TAuthorization(
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
    authorization = types.TAuthorization(
        public_key="public key 1", secret_key=secret_key
    )
    auth_info = types.CredentialsAuthInfo(
        sub="sub 1", secret_key_hash=secret_key_hash, salt=salt
    )

    library.authorize_user(authorization=authorization, auth_info=auth_info)


CALCULATE_REQUEST_TYPE_ERROR_TESTS = [
    pytest.param("", id="no /"),
    pytest.param("/", id="single /"),
    pytest.param("///", id="too many /"),
]


@pytest.mark.parametrize("uri", CALCULATE_REQUEST_TYPE_ERROR_TESTS)
def test_calculate_request_type_error(uri):
    """
    GIVEN invalid uri
    WHEN calculate_request_type is called with the uri
    THEN NotFoundError is raises.
    """
    with pytest.raises(exceptions.NotFoundError):
        library.calculate_request_type(uri=uri)


CALCULATE_REQUEST_TYPE_TESTS = [
    pytest.param("/spec 1/", types.TRequestType.LIST, id="list"),
    pytest.param("/spec 1/package.tar.gz", types.TRequestType.INSTALL, id="install"),
]


@pytest.mark.parametrize("uri, expected_type", CALCULATE_REQUEST_TYPE_TESTS)
def test_calculate_request_type(uri, expected_type):
    """
    GIVEN uri
    WHEN calculate_request_type is called with the uri
    THEN the expected type is returned.
    """
    returned_type = library.calculate_request_type(uri=uri)

    assert returned_type == expected_type


def test_create_list_response_value_error(_clean_specs_table):
    """
    GIVEN empty database and uri
    WHEN create_list_response_value is called with the uri
    THEN NotFoundError is raised.
    """
    uri = "/spec 1/"
    auth_info = types.CredentialsAuthInfo(
        sub="sub 1", secret_key_hash=b"secret key 1", salt=b"salt 1"
    )
    authorization = types.TAuthorization(
        public_key="public key 1", secret_key="secret key 1"
    )

    with pytest.raises(exceptions.NotFoundError):
        library.create_list_response_value(
            authorization=authorization, uri=uri, auth_info=auth_info
        )


def test_create_list_response_value(_clean_specs_table, monkeypatch):
    """
    GIVEN database with single then multiple specs and uri that points to the spec
    WHEN create_list_response_value is called with the uri
    THEN a HTML response with links to the packages are returned.
    """
    mock_time = mock.MagicMock()
    monkeypatch.setattr(time, "time", mock_time)
    mock_time.return_value = 1000000
    spec_id = "spec 1"
    version_1 = "version 1"
    uri = f"/{spec_id}/"
    sub = "sub 1"
    auth_info = types.CredentialsAuthInfo(
        sub=sub, secret_key_hash=b"secret key 1", salt=b"salt 1"
    )
    public_key = "public key 1"
    secret_key = "secret key 1"
    authorization = types.TAuthorization(public_key=public_key, secret_key=secret_key)
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version_1, model_count=1
    )

    returned_value = library.create_list_response_value(
        authorization=authorization, uri=uri, auth_info=auth_info
    )

    assert "<body>" in returned_value
    assert (
        '<a href="https://'
        f"{public_key}:{secret_key}"
        "@index.package.openalchemy.io/"
        f'{spec_id}/{spec_id}-{version_1}.tar.gz">'
        f"{spec_id}-{version_1}.tar.gz</a><br>"
    ) in returned_value
    assert "</body>" in returned_value

    mock_time.return_value = 2000000
    version_2 = "version 2"
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version_2, model_count=1
    )

    returned_value = library.create_list_response_value(
        authorization=authorization, uri=uri, auth_info=auth_info
    )

    assert (
        '<a href="https://'
        f"{public_key}:{secret_key}"
        "@index.package.openalchemy.io/"
        f'{spec_id}/{spec_id}-{version_1}.tar.gz">'
        f"{spec_id}-{version_1}.tar.gz</a><br>"
    ) in returned_value
    assert (
        '<a href="https://'
        f"{public_key}:{secret_key}"
        "@index.package.openalchemy.io/"
        f'{spec_id}/{spec_id}-{version_2}.tar.gz">'
        f"{spec_id}-{version_2}.tar.gz</a><br>"
    ) in returned_value


def test_create_install_response_value():
    """
    GIVEN uri and authorization value
    WHEN create_install_response_value is called
    THEN the uri prefixed with the user is returned.
    """
    uri = "/uri 1"
    sub = "sub 1"
    auth_info = types.CredentialsAuthInfo(
        sub=sub, secret_key_hash=b"secret key 1", salt=b"salt 1"
    )

    returned_value = library.create_install_response_value(uri=uri, auth_info=auth_info)

    assert returned_value == f"/{sub}{uri}"


def test_create_response_list(_clean_specs_table):
    """
    GIVEN database with single spec and list type request, authorization info and uri
    WHEN create_response is called with the type, uri and authorization info
    THEN a list response is returned.
    """
    spec_id = "spec 1"
    version = "version 1"
    uri = f"/{spec_id}/"
    sub = "sub 1"
    auth_info = types.CredentialsAuthInfo(
        sub=sub, secret_key_hash=b"secret key 1", salt=b"salt 1"
    )
    request_type = types.TRequestType.LIST
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version, model_count=1
    )
    public_key = "public key 1"
    secret_key = "secret key 1"
    authorization = types.TAuthorization(public_key=public_key, secret_key=secret_key)

    returned_response = library.create_response(
        authorization=authorization,
        request_type=request_type,
        uri=uri,
        auth_info=auth_info,
    )

    assert returned_response.type == request_type
    assert "<body>" in returned_response.value
    assert spec_id in returned_response.value
    assert version in returned_response.value
    assert public_key in returned_response.value
    assert secret_key in returned_response.value


def test_create_response_install():
    """
    GIVEN install type request, authorization info and uri
    WHEN create_response is called with the type, uri and authorization info
    THEN an install response is returned.
    """
    uri = "uri 1"
    sub = "sub 1"
    auth_info = types.CredentialsAuthInfo(
        sub=sub, secret_key_hash=b"secret key 1", salt=b"salt 1"
    )
    request_type = types.TRequestType.INSTALL
    public_key = "public key 1"
    secret_key = "secret key 1"
    authorization = types.TAuthorization(public_key=public_key, secret_key=secret_key)

    returned_response = library.create_response(
        authorization=authorization,
        request_type=request_type,
        uri=uri,
        auth_info=auth_info,
    )

    assert returned_response.type == request_type
    assert uri in returned_response.value
    assert sub in returned_response.value


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
        library.process(uri="", authorization_value=authorization_value)


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
    spec_id = "spec 1"
    version = "version 1"
    uri = f"/{spec_id}/{spec_id}-{version}.tar.gz"
    credentials = factory.CredentialsFactory(secret_key_hash=secret_key_hash, salt=salt)
    credentials.save()
    token = base64.b64encode(f"{credentials.public_key}:{secret_key}".encode()).decode()
    authorization_value = f"Basic {token}"

    library.process(uri=uri, authorization_value=authorization_value)

"""Tests for the app."""

import base64
import copy

import app
import pytest
from open_alchemy import package_database, package_security
from open_alchemy.package_database import factory

PARSE_REQUEST_ERROR_TESTS = [
    pytest.param({}, id="headers missing"),
    pytest.param({"headers": None, "uri": "uri 1"}, id="headers not dict"),
    pytest.param({"headers": {}, "uri": "uri 1"}, id="headers authorization missing"),
    pytest.param(
        {"headers": {"authorization": None}, "uri": "uri 1"},
        id="headers authorization not list",
    ),
    pytest.param(
        {"headers": {"authorization": []}, "uri": "uri 1"},
        id="headers authorization empty",
    ),
    pytest.param(
        {"headers": {"authorization": [None, None]}, "uri": "uri 1"},
        id="headers authorization multiple",
    ),
    pytest.param(
        {"headers": {"authorization": [None]}, "uri": "uri 1"},
        id="headers authorization item not dict",
    ),
    pytest.param(
        {"headers": {"authorization": [{}]}, "uri": "uri 1"},
        id="headers authorization item value missing",
    ),
    pytest.param(
        {"headers": {"authorization": [{"value": None}]}, "uri": "uri 1"},
        id="headers authorization item value not string",
    ),
    pytest.param(
        {"headers": {"authorization": [{"value": "value 1"}]}},
        id="uri missing",
    ),
    pytest.param(
        {"uri": None, "headers": {"authorization": [{"value": "value 1"}]}},
        id="uri not string",
    ),
]


@pytest.mark.parametrize("request_", PARSE_REQUEST_ERROR_TESTS)
def test_parse_request_error(request_):
    """
    GIVEN request that is not valid
    WHEN parse_request is called with the request
    THEN AssertionError is raised.
    """
    with pytest.raises(AssertionError):
        app.parse_request(request=request_, event_prefix="", event={})


def test_parse_request():
    """
    GIVEN lambda event request
    WHEN parse_request is called with the request
    THEN the authorization value and uri are returned.
    """
    authorization_value = "value 1"
    uri = "uri 1"
    request = {
        "uri": uri,
        "headers": {"authorization": [{"value": authorization_value}]},
    }

    returned_request = app.parse_request(request=request, event_prefix="", event={})

    assert returned_request.authorization_value == authorization_value
    assert returned_request.uri == uri


PARSE_EVENT_ERROR_TESTS = [
    pytest.param(None, id="not dict"),
    pytest.param({}, id="Records missing"),
    pytest.param({"Records": None}, id="Records not list"),
    pytest.param({"Records": []}, id="Records empty"),
    pytest.param({"Records": [None, None]}, id="Records multiple items"),
    pytest.param({"Records": [None]}, id="Records item not dict"),
    pytest.param({"Records": [{}]}, id="Records item cf missing"),
    pytest.param({"Records": [{"cf": None}]}, id="Records item cf not dict"),
    pytest.param({"Records": [{"cf": {}}]}, id="Records item cf request missing"),
    pytest.param(
        {"Records": [{"cf": {"request": None}}]}, id="Records item cf request not dict"
    ),
    pytest.param({"Records": [{"cf": {"request": {}}}]}, id="Records headers missing"),
]


@pytest.mark.parametrize("event", PARSE_EVENT_ERROR_TESTS)
def test_parse_event_error(event):
    """
    GIVEN event that is not valid
    WHEN parse_event is called with the event
    THEN AssertionError is raised.
    """
    with pytest.raises(AssertionError):
        app.parse_event(event=event)


def test_parse_event():
    """
    GIVEN lambda event event
    WHEN parse_event is called with the event
    THEN the authorization value and uri are returned.
    """
    authorization_value = "value 1"
    uri = "uri 1"
    request = {
        "headers": {
            "authorization": [{"key": "Authorization", "value": authorization_value}]
        },
        "uri": uri,
    }
    event = {"Records": [{"cf": {"request": copy.deepcopy(request)}}]}

    returned_event = app.parse_event(event=event)

    assert returned_event.request.authorization_value == authorization_value
    assert returned_event.request.uri == uri
    assert returned_event.request_dict == request


def test_main_list(_clean_credentials_table, _clean_specs_table):
    """
    GIVEN list event
    WHEN main is called with the event
    THEN a list response is returned.
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
    spec_id = "spec 1"
    version = "version 1"
    uri = f"/{spec_id}/"
    package_database.get().create_update_spec(
        sub=credentials.sub, id_=spec_id, version=version, model_count=1
    )
    request = {
        "headers": {
            "authorization": [{"key": "Authorization", "value": authorization_value}]
        },
        "uri": uri,
    }
    event = {"Records": [{"cf": {"request": copy.deepcopy(request)}}]}

    returned_response = app.main(event, None)

    assert returned_response["status"] == "200"
    assert returned_response["statusDescription"] == "OK"
    assert returned_response["headers"]["cache-control"][0]["value"] == "max-age=0"
    assert returned_response["headers"]["content-type"][0]["value"] == "text/html"
    assert spec_id in returned_response["body"]
    assert version in returned_response["body"]


def test_main_install(_clean_credentials_table):
    """
    GIVEN install event
    WHEN main is called with the event
    THEN a install response is returned.
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
    spec_id = "spec 1"
    version = "version 1"
    uri = f"/{spec_id}/{spec_id}-{version}.tar.gz"
    request = {
        "headers": {
            "authorization": [{"key": "Authorization", "value": authorization_value}]
        },
        "uri": uri,
    }
    event = {"Records": [{"cf": {"request": copy.deepcopy(request)}}]}

    returned_response = app.main(event, None)

    assert returned_response == {**request, "uri": f"/{credentials.sub}{uri}"}

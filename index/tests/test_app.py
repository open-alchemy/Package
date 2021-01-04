"""Tests for the app."""

import app
import pytest

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

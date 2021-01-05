"""Tests for the pytest plugin."""


def test_access_token(access_token):
    """
    GIVEN TEST_USERNAME and TEST_PASSWORD environment variables are set
    WHEN the access_token fixture is requested
    THEN an access token is returned.
    """
    assert access_token

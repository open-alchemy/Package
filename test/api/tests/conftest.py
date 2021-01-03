"""Fixtures for the API."""

# pylint: disable=redefined-outer-name

import os
from urllib import request

import boto3
import pytest


@pytest.fixture(scope="session")
def access_token():
    """Get an access token."""
    cognito = boto3.client("cognito-idp")

    user_pool_id = os.getenv("USER_POOL_ID")
    if user_pool_id is None:
        raise AssertionError("USER_POOL_ID environment variable not defined")

    client_id = os.getenv("CLIENT_ID")
    if client_id is None:
        raise AssertionError("CLIENT_ID environment variable not defined")

    test_username = os.getenv("TEST_USERNAME")
    if test_username is None:
        raise AssertionError("TEST_USERNAME environment variable not defined")
    test_password = os.getenv("TEST_PASSWORD")
    if test_password is None:
        raise AssertionError("TEST_PASSWORD environment variable not defined")

    auth_flow = "ADMIN_USER_PASSWORD_AUTH"

    response = cognito.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow=auth_flow,
        AuthParameters={"USERNAME": test_username, "PASSWORD": test_password},
    )

    yield response["AuthenticationResult"]["AccessToken"]


@pytest.fixture()
def spec_id(access_token):
    """Returns a spec id that is cleaned up at the end."""
    spec_id = "specId1"

    yield spec_id

    delete_request = request.Request(
        f"https://package.api.openalchemy.io/v1/specs/{spec_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        method="DELETE",
    )
    with request.urlopen(delete_request) as response:
        assert response.status == 204


@pytest.fixture()
def credentials_id(access_token):
    """Returns a credentials id that is cleaned up at the end."""
    credentials_id = "default"

    yield credentials_id

    delete_request = request.Request(
        f"https://package.api.openalchemy.io/v1/credentials/{credentials_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        method="DELETE",
    )
    with request.urlopen(delete_request) as response:
        assert response.status == 204

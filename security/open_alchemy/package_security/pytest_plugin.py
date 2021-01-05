"""Useful pytest fixtures."""
# pylint: disable=unused-argument,redefined-outer-name

import os

import boto3
import pytest

from . import config


@pytest.fixture(scope="session")
def service_secret():
    """Set the service secret."""
    service_secret = b"service secret 1"

    config_instance = config.get()
    config_instance.service_secret = service_secret

    yield service_secret

    config_instance.service_secret = None


@pytest.fixture(scope="session")
def _service_secret(service_secret):
    """Unused argument version of service_secret."""


@pytest.fixture(scope="session")
def access_token():
    """Get an access token."""
    ssm = boto3.client("ssm")
    user_pool_id = ssm.get_parameter(Name="/Editor/Identity/UserPool/Id")["Parameter"][
        "Value"
    ]
    client_id = ssm.get_parameter(Name="/Editor/Identity/UserPool/Client/Admin/Id")[
        "Parameter"
    ]["Value"]

    cognito = boto3.client("cognito-idp")

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

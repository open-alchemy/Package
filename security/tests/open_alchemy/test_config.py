"""Tests for configuration."""

from unittest import mock

import pytest
from botocore import stub
from open_alchemy.package_security import config

SERVICE_SECRET_ERROR_TESTS = [
    pytest.param(None, id="secretsmanager response not dict"),
    pytest.param({}, id="secretsmanager response SecretBinary missing"),
    pytest.param(
        {"SecretBinary": None}, id="secretsmanager response SecretBinary not bytes"
    ),
]


@pytest.mark.parametrize("return_value", SERVICE_SECRET_ERROR_TESTS)
def test_service_secret_error(monkeypatch, return_value):
    """
    GIVEN monkeypatched AWS secretsmanager where get_secret_value response is invalid
    WHEN service_secret is retrieved from the configuration
    THEN the secret value is not retrieved from AWS.
    """
    # pylint: disable=protected-access
    mock_get_secret_value = mock.MagicMock()
    mock_get_secret_value.return_value = return_value
    monkeypatch.setattr(
        config._SECRETS_MANAGER_CLIENT, "get_secret_value", mock_get_secret_value
    )

    config_instance = config._get()
    with pytest.raises(AssertionError):
        config_instance.service_secret  # pylint: disable=pointless-statement


def test_service_secret_not_set():
    """
    GIVEN stubbed AWS secretsmanager
    WHEN service_secret is retrieved from the configuration twice
    THEN the secret value is retrieved from secretsmanager once.
    """
    # pylint: disable=protected-access
    config_instance = config._get()
    secret_binary = b"secret binary 1"

    stubber = stub.Stubber(config._SECRETS_MANAGER_CLIENT)
    expected_params = {"SecretId": config_instance.service_secret_name}
    stubber.add_response(
        "get_secret_value", {"SecretBinary": secret_binary}, expected_params
    )
    stubber.activate()

    service_secret = config_instance.service_secret

    stubber.assert_no_pending_responses()
    assert service_secret == secret_binary

    service_secret = config_instance.service_secret

    assert service_secret == secret_binary


def test_service_secret_set(monkeypatch):
    """
    GIVEN monkeypatched AWS secretsmanager and config with service_secret set
    WHEN service_secret is retrieved from the configuration
    THEN the secret value is not retrieved from AWS.
    """
    # pylint: disable=protected-access
    service_secret = "service secret 1"
    mock_get_secret_value = mock.MagicMock()
    monkeypatch.setattr(
        config._SECRETS_MANAGER_CLIENT, "get_secret_value", mock_get_secret_value
    )

    config_instance = config._get()
    config_instance.service_secret = service_secret
    returned_service_secret = config_instance.service_secret

    mock_get_secret_value.assert_not_called()
    assert returned_service_secret == service_secret

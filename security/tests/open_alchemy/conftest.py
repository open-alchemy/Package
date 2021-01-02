"""Fixtures for tests."""

import pytest
from open_alchemy.package_security import config


@pytest.fixture(scope="session", autouse=True)
def set_service_secret():
    """Set the service secret."""
    service_secret = b"service secret 1"

    config_instance = config.get()
    config_instance.service_secret = service_secret

    yield service_secret

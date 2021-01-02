"""Useful pytest fixtures."""
# pylint: disable=unused-argument,redefined-outer-name

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

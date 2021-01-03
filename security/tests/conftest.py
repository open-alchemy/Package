"""Common fixtures."""

import pytest

pytest_plugins = (  # pylint: disable=invalid-name
    "open_alchemy.package_security.pytest_plugin"
)


@pytest.fixture(scope="session", autouse=True)
def use_service_secret(_service_secret):
    """Automatically use the _service_secret fixture."""

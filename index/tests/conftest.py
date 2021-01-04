"""Shared fixtures."""

import pytest


@pytest.fixture(scope="session", autouse=True)
def use_service_secret(_service_secret):
    """Automatically uses the _service_secret fixture from package-security."""

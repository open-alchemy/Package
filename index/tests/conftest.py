"""Shared fixtures."""

import pytest


@pytest.fixture(scope="session", autouse=True)
def use_service_secret(_service_secret):
    """Automatically uses the _service_secret fixture from package-security."""


@pytest.fixture(autouse=True)
def override_stage(monkeypatch):
    """Overrides the STAGE environment variable."""
    monkeypatch.setenv("STAGE", "TEST")

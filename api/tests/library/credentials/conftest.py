"""Fixtures for credentials."""

import pytest


@pytest.fixture(autouse=True)
def use_clean_credentials_table(_clean_credentials_table):
    """Uses the _clean_credentials_table fixture for all tests."""


@pytest.fixture(autouse=True, scope="session")
def use_service_secret(_service_secret):
    """Uses the _service_secret fixture for all tests."""

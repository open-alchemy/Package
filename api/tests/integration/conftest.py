"""Fixtures for API."""

import pytest
from app import app


@pytest.fixture(scope="module")
def client():
    """Create test client for app."""
    with app.app.test_client() as test_client:
        yield test_client

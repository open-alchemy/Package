"""Fixtures."""

import uuid

import pytest
from open_alchemy import package_database


@pytest.fixture
def sub():
    """Generates a sub and cleans up after any tests."""
    sub_value = f"test.{uuid.uuid4()}"

    yield sub_value

    package_database.get().delete_all(sub=sub_value)

"""Fixtures."""

import pytest
from open_alchemy import package_database


@pytest.fixture
def sub():
    """Generates a sub and cleans up after any tests."""
    sub_value = "test.sub 1"

    yield sub_value

    package_database.get().delete_all_credentials(sub=sub_value)
    package_database.get().delete_all_specs(sub=sub_value)

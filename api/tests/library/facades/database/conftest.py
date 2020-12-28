"""Database fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _auto_clean_package_table(_clean_package_storage_table):
    """Autouses _clean_package_storage_table."""

"""Database fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _auto_clean_credentials_table(_clean_credentials_table):
    """Autouses _clean_credentials_table."""

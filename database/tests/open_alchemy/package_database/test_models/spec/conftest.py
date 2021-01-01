"""Database fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _auto_clean_spec_table(_clean_spec_table):
    """Autouses _clean_spec_table."""

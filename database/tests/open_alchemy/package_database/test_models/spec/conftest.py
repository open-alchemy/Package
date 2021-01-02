"""Database fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _auto_clean_specs_table(_clean_specs_table):
    """Autouses _clean_specs_table."""

"""Fixtures for database tests."""

import subprocess

import pytest


@pytest.fixture(autouse=True, scope="module")
def test_database():
    """Starts the database server."""
    process = subprocess.Popen(
        ["npx", "node", "tests/library/facades/database/init-database.js"]
    )

    yield "http://localhost:8000"

    process.terminate()

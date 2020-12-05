"""Fixtures for database tests."""

from urllib import request, error
import subprocess

import pytest

from library.facades.database import models


@pytest.fixture(scope="module")
def _database():
    """Starts the database server."""
    process = subprocess.Popen(
        ["npx", "node", "tests/library/facades/database/init-database.js"]
    )
    url = "http://localhost:8000"

    # Wait for the server to be available
    head_request = request.Request(url, method="HEAD")
    for _ in range(10):
        try:
            request.urlopen(head_request)
        except error.URLError:
            pass

    yield url

    process.terminate()


@pytest.fixture(scope="module")
def _package_store_table(_database):
    """Create the package-store table and empty it after every test."""
    models.PackageStorage.create_table(read_capacity_units=1, write_capacity_units=1)


@pytest.fixture()
def _clean_package_store_table(_package_store_table):
    """Create the package-store table and empty it after every test."""
    yield

    with models.PackageStorage.batch_write() as batch:
        for item in models.PackageStorage.scan():
            batch.delete(item)

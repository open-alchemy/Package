"""Fixtures for database tests."""

import subprocess
import time

from pynamodb import connection, exceptions
import pytest

from library.facades.database import models


@pytest.fixture(scope="module")
def _database():
    """Starts the database server."""
    process = subprocess.Popen(
        ["npx", "node", "tests/library/facades/database/init-database.js"]
    )
    host = "http://localhost:8000"

    # Wait for the server to be available
    started = False
    for _ in range(100):
        try:
            conn = connection.Connection(host=host)
            conn.list_tables()
            started = True
            break
        except exceptions.PynamoDBConnectionError:
            time.sleep(0.001)
            pass
    if not started:
        process.terminate()
        process.wait(timeout=10)
        process.kill()
        process.wait(timeout=10)
        if not process.poll() is not None:
            raise AssertionError(
                "could not start the database server and failed to terminate process, "
                f"pid: {process.pid}"
            )
        raise AssertionError(
            f"could not start the database server, stdout: {process.stdout.read()}, "
            f"stderr: {process.stderr.read()}"
        )

    yield host

    process.terminate()
    process.wait(timeout=10)
    process.kill()
    process.wait(timeout=10)
    if not process.poll() is not None:
        raise AssertionError(
            f"could not terminate the database server process, pid: {process.pid}"
        )


@pytest.fixture(scope="module")
def _package_storage_table(_database):
    """Create the package-storage table and empty it after every test."""
    models.PackageStorage.create_table(read_capacity_units=1, write_capacity_units=1)


@pytest.fixture()
def _clean_package_storage_table(_package_storage_table):
    """Create the package-storage table and empty it after every test."""
    yield

    with models.PackageStorage.batch_write() as batch:
        for item in models.PackageStorage.scan():
            batch.delete(item)

"""Common fixtures."""

import subprocess

import pytest
from library.facades import storage
from library.facades.database import models
from pynamodb import connection, exceptions


@pytest.fixture(scope="session")
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
        raise AssertionError("could not start the database server")

    yield host

    process.terminate()
    process.wait(timeout=10)
    process.kill()
    process.wait(timeout=10)
    if not process.poll() is not None:
        raise AssertionError(
            f"could not terminate the database server process, pid: {process.pid}"
        )


@pytest.fixture(scope="session")
def _package_storage_table(_database):
    """Create the package-storage table and empty it after every test."""
    assert not models.PackageStorage.exists()
    models.PackageStorage.create_table(
        read_capacity_units=1,
        write_capacity_units=1,
        wait=True,
    )

    yield


@pytest.fixture()
def _clean_package_storage_table(_package_storage_table):
    """Create the package-storage table and empty it after every test."""
    yield

    with models.PackageStorage.batch_write() as batch:
        for item in models.PackageStorage.scan():
            batch.delete(item)


@pytest.fixture(autouse=True)
def clean_storage():
    """Delete all objects from the storage."""
    # pylint: disable=protected-access

    yield

    keys = storage._STORAGE.list()

    storage._STORAGE.delete_all(keys=keys)

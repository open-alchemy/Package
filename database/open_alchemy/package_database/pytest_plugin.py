"""Common fixtures."""

import pathlib
import subprocess

import pytest
from open_alchemy.package_database import models
from pynamodb import connection, exceptions


@pytest.fixture(scope="session")
def _database():
    """Starts the database server."""
    init_database_script = pathlib.Path(__file__).parent / "init-database.js"
    process = subprocess.Popen(["npx", "node", str(init_database_script)])
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
def _specs_table(_database):
    """Create the specs table and empty it after every test."""
    assert not models.Spec.exists()
    models.Spec.create_table(
        read_capacity_units=1,
        write_capacity_units=1,
        wait=True,
    )

    yield

    models.Spec.delete_table()


@pytest.fixture()
def _clean_specs_table(_specs_table):
    """Create the specs table and empty it after every test."""
    with models.Spec.batch_write() as batch:
        for item in models.Spec.scan():
            batch.delete(item)

    yield

    with models.Spec.batch_write() as batch:
        for item in models.Spec.scan():
            batch.delete(item)


@pytest.fixture(scope="session")
def _credentials_table(_database):
    """Create the credentials table and empty it after every test."""
    assert not models.Credentials.exists()
    models.Credentials.create_table(
        read_capacity_units=1,
        write_capacity_units=1,
        wait=True,
    )

    yield

    models.Credentials.delete_table()


@pytest.fixture()
def _clean_credentials_table(_credentials_table):
    """Create the credentials table and empty it after every test."""
    with models.Credentials.batch_write() as batch:
        for item in models.Credentials.scan():
            batch.delete(item)

    yield

    with models.Credentials.batch_write() as batch:
        for item in models.Credentials.scan():
            batch.delete(item)

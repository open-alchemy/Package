"""Common fixtures."""

import pytest
from library.facades import storage


@pytest.fixture(autouse=True)
def clean_storage():
    """Delete all objects from the storage."""
    # pylint: disable=protected-access

    yield

    keys = storage._STORAGE.list()

    storage._STORAGE.delete_all(keys=keys)

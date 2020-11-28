"""Common fixtures."""

import pytest

from library.facades import storage


@pytest.fixture(autouse=True)
def clean_storage():
    """Delete all objects from the storage."""
    yield

    keys = storage.get_storage().list()

    for key in keys:
        storage.get_storage().delete(key=key)

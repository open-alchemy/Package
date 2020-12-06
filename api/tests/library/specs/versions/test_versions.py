"""Tests for the specs endpoint."""

import json
from unittest import mock

from library.specs import versions
from library.facades import storage


def test_list_():
    """
    GIVEN user, spec id and storage with a single spec
    WHEN list_ is called with the user and spec id
    THEN the version of the spec is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version = "version 1"
    storage.get_storage().create_update_spec(
        user=user, spec_id=spec_id, version=version, spec_str="spec str 1"
    )

    response = versions.list_(user=user, spec_id=spec_id)

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert json.loads(response.data.decode()) == [version]


def test_list_not_found():
    """
    GIVEN user, spec id and empty storage
    WHEN list_ is called with the user and spec id
    THEN 404 is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"

    response = versions.list_(user=user, spec_id=spec_id)

    assert response.status_code == 404
    assert response.mimetype == "text/plain"
    assert spec_id in response.data.decode()


def test_list_storage_error(monkeypatch):
    """
    GIVEN user, spec id and storage that raises a StorageError
    WHEN list_ is called with the user and spec id
    THEN 500 is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    mock_storage_get_spec_versions = mock.MagicMock()
    mock_storage_get_spec_versions.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(
        storage.get_storage(), "get_spec_versions", mock_storage_get_spec_versions
    )

    response = versions.list_(user=user, spec_id=spec_id)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "storage" in response.data.decode()

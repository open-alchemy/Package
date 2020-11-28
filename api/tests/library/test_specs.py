"""Tests for the specs endpoint."""

from unittest import mock

from library import specs
from library.facades import storage


def test_put():
    """
    GIVEN body and spec id
    WHEN put is called with the body and spec id
    THEN the spec is stored against the spec id.
    """
    body = "body 1"
    spec_id = "id 1"

    response = specs.put(body=body.encode(), spec_id=spec_id)

    assert storage.get_storage().get(key=f"{spec_id}/spec.json") == body
    assert response.status_code == 204


def test_put_error(monkeypatch):
    """
    GIVEN body and spec id
    WHEN put is called with the body and spec id
    THEN the spec is stored against the spec id.
    """
    body = "body 1"
    spec_id = "id 1"
    mock_storage_set = mock.MagicMock()
    mock_storage_set.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(storage.get_storage(), "set", mock_storage_set)

    response = specs.put(body=body.encode(), spec_id=spec_id)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"

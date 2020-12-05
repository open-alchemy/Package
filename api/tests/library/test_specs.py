"""Tests for the specs endpoint."""

import json

from unittest import mock

from library import specs
from library.facades import storage, server, database


def test_list_(_clean_package_storage_table):
    """
    GIVEN user and database with a single spec
    WHEN list_ is called with the user
    THEN all the specs stored on the user are returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    database.get_database().create_update_spec(
        sub=user, spec_id=spec_id, version="version 1", model_count=1
    )

    response = specs.list_(user=user)

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert json.loads(response.data.decode()) == [spec_id]


def test_list_miss(_clean_package_storage_table):
    """
    GIVEN user and database with a single spec for a different user
    WHEN list_ is called with the user
    THEN empty list is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    database.get_database().create_update_spec(
        sub="user 2", spec_id=spec_id, version="version 1", model_count=1
    )

    response = specs.list_(user=user)

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert json.loads(response.data.decode()) == []


def test_list_database_error(monkeypatch):
    """
    GIVEN user and database that raises a DatabaseError
    WHEN list_ is called with the user
    THEN a 500 is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    mock_database_list_specs = mock.MagicMock()
    mock_database_list_specs.side_effect = database.exceptions.DatabaseError
    monkeypatch.setattr(
        database.get_database(),
        "list_specs",
        mock_database_list_specs,
    )

    response = specs.list_(user=user)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


def test_put(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body and spec id
    WHEN put is called with the body and spec id
    THEN the spec is stored against the spec id.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    body = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    user = "user 1"

    response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

    assert storage.get_storage().get(
        key=f"{user}/{spec_id}/{version}-spec.json"
    ) == json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))
    assert database.get_database().count_customer_models(sub=user) == 1
    assert response.status_code == 204


def test_put_invalid_spec_error(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body with invalid spec and spec id
    WHEN put is called with the body and spec id
    THEN a 400 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    body = "body 1"
    spec_id = "id 1"
    user = "user 1"

    response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

    assert response.status_code == 400
    assert response.mimetype == "text/plain"
    assert "not valid" in response.data.decode()


def test_put_too_many_models_error(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body spec and spec id and user that already has too many models
    WHEN put is called with the body and spec id
    THEN a 402 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    body = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    user = "user 1"
    database.get_database().create_update_spec(
        sub=user, spec_id=spec_id, version="version 1", model_count=100
    )

    response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

    assert response.status_code == 402
    assert response.mimetype == "text/plain"
    assert "exceeded" in response.data.decode()
    assert ": 100," in response.data.decode()
    assert "spec: 1" in response.data.decode()


def test_put_database_count_error(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body with invalid spec and spec id and database that raises DatabaseError
    WHEN put is called with the body and spec id
    THEN a 500 is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    body = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    user = "user 1"
    mock_database_count_customer_models = mock.MagicMock()
    mock_database_count_customer_models.side_effect = database.exceptions.DatabaseError
    monkeypatch.setattr(
        database.get_database(),
        "count_customer_models",
        mock_database_count_customer_models,
    )

    response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


def test_put_storage_error(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body with invalid spec and spec id
    WHEN put is called with the body and spec id
    THEN a 400 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    body = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    user = "user 1"
    mock_storage_set = mock.MagicMock()
    mock_storage_set.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(storage.get_storage(), "set", mock_storage_set)

    response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "storing" in response.data.decode()


def test_put_database_update_error(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body and spec id
    WHEN put is called with the body and spec id
    THEN the spec is stored against the spec id.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    body = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    user = "user 1"
    mock_database_create_update_spec = mock.MagicMock()
    mock_database_create_update_spec.side_effect = database.exceptions.DatabaseError
    monkeypatch.setattr(
        database.get_database(),
        "create_update_spec",
        mock_database_create_update_spec,
    )

    response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

    assert storage.get_storage().get(
        key=f"{user}/{spec_id}/{version}-spec.json"
    ) == json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))
    assert database.get_database().count_customer_models(sub=user) == 0
    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()

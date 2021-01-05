"""Tests for the specs endpoint."""

import json
from unittest import mock

import pytest
from library import specs
from library.facades import server, storage
from open_alchemy import package_database


@pytest.mark.specs
def test_list_(_clean_specs_table):
    """
    GIVEN user and database with a single spec
    WHEN list_ is called with the user
    THEN all the specs stored on the user are returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    model_count = 1
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=model_count
    )

    response = specs.list_(user=user)

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    spec_infos = json.loads(response.data.decode())
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["name"] == spec_name
    assert spec_info["id"] == spec_name
    assert spec_info["version"] == version
    assert spec_info["model_count"] == model_count
    assert "updated_at" in spec_info


@pytest.mark.specs
def test_list_miss(_clean_specs_table):
    """
    GIVEN user and database with a single spec for a different user
    WHEN list_ is called with the user
    THEN empty list is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    package_database.get().create_update_spec(
        sub="user 2", name=spec_name, version="1", model_count=1
    )

    response = specs.list_(user=user)

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert json.loads(response.data.decode()) == []


@pytest.mark.specs
def test_list_database_error(monkeypatch):
    """
    GIVEN user and database that raises a DatabaseError
    WHEN list_ is called with the user
    THEN a 500 is returned.
    """
    user = "user 1"
    mock_database_list_specs = mock.MagicMock()
    mock_database_list_specs.side_effect = package_database.exceptions.BaseError
    monkeypatch.setattr(
        package_database.get(),
        "list_specs",
        mock_database_list_specs,
    )

    response = specs.list_(user=user)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


@pytest.mark.specs
def test_get(_clean_specs_table):
    """
    GIVEN user and database and storage with a single spec
    WHEN get is called with the user and spec id
    THEN the spec value is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=1
    )
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=user,
        name=spec_name,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )

    response = specs.get(user=user, spec_name=spec_name)

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert f"version: '{version}'" in response.data.decode()
    assert "key: value" in response.data.decode()


@pytest.mark.specs
def test_get_database_error(_clean_specs_table, monkeypatch):
    """
    GIVEN user and database that raises an error
    WHEN get is called with the user and spec id
    THEN a 500 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    mock_database_get_latest_spec_version = mock.MagicMock()
    mock_database_get_latest_spec_version.side_effect = (
        package_database.exceptions.BaseError
    )
    monkeypatch.setattr(
        package_database.get(),
        "get_latest_spec_version",
        mock_database_get_latest_spec_version,
    )

    response = specs.get(user=user, spec_name=spec_name)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


@pytest.mark.specs
def test_get_database_miss(_clean_specs_table):
    """
    GIVEN user and empty database
    WHEN get is called with the user and spec id
    THEN a 404 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"

    response = specs.get(user=user, spec_name=spec_name)

    assert response.status_code == 404
    assert response.mimetype == "text/plain"
    assert spec_name in response.data.decode()
    assert "not find" in response.data.decode()


@pytest.mark.specs
def test_get_storage_facade_error(_clean_specs_table, monkeypatch):
    """
    GIVEN user and database with a spec but storage that raises an error
    WHEN get is called with the user and spec id
    THEN a 500 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=1
    )
    mock_storage_get_spec = mock.MagicMock()
    mock_storage_get_spec.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(storage.get_storage_facade(), "get_spec", mock_storage_get_spec)

    response = specs.get(user=user, spec_name=spec_name)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "reading" in response.data.decode()


@pytest.mark.specs
def test_get_storage_facade_miss(_clean_specs_table):
    """
    GIVEN user and database with a spec but empty storage
    WHEN get is called with the user and spec id
    THEN a 404 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=1
    )

    response = specs.get(user=user, spec_name=spec_name)

    assert response.status_code == 404
    assert response.mimetype == "text/plain"
    assert spec_name in response.data.decode()
    assert "not find" in response.data.decode()


@pytest.mark.specs
def test_put(monkeypatch, _clean_specs_table):
    """
    GIVEN body, spec id and user
    WHEN put is called with the body, spec id and user
    THEN the spec is stored against the spec id.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "1"
    title = "title 1"
    description = "description 1"
    spec = {
        "info": {"version": version, "title": title, "description": description},
        "components": {
            "schemas": {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        },
    }
    body = json.dumps(spec)
    spec_name = "id 1"
    user = "user 1"

    response = specs.put(body=body.encode(), spec_name=spec_name, user=user)

    spec_str = storage.get_storage_facade().get_spec(
        user=user, name=spec_name, version=version
    )
    assert f'"{version}"' in spec_str
    assert '"Schema"' in spec_str
    assert '"x-tablename"' in spec_str
    assert '"schema"' in spec_str

    assert package_database.get().count_customer_models(sub=user) == 1
    spec_infos = package_database.get().list_specs(sub=user)
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["name"] == spec_name
    assert spec_info["id"] == spec_name
    assert spec_info["version"] == version
    assert spec_info["title"] == title
    assert spec_info["description"] == description
    assert spec_info["model_count"] == 1
    assert "updated_at" in spec_info

    assert response.status_code == 204


@pytest.mark.specs
def test_put_invalid_spec_error(monkeypatch):
    """
    GIVEN body with invalid spec and spec id and user
    WHEN put is called with the body, spec id and user
    THEN a 400 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    body = "body 1"
    spec_name = "id 1"
    user = "user 1"

    response = specs.put(body=body.encode(), spec_name=spec_name, user=user)

    assert response.status_code == 400
    assert response.mimetype == "text/plain"
    assert "not valid" in response.data.decode()


@pytest.mark.specs
def test_put_too_many_models_error(monkeypatch, _clean_specs_table):
    """
    GIVEN body spec and spec id and user that already has too many models
    WHEN put is called with the body and spec id
    THEN a 402 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "1"
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
    spec_name = "id 1"
    user = "user 1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version="1", model_count=100
    )

    response = specs.put(body=body.encode(), spec_name=spec_name, user=user)

    assert response.status_code == 402
    assert response.mimetype == "text/plain"
    assert "exceeded" in response.data.decode()
    assert ": 100," in response.data.decode()
    assert "spec: 1" in response.data.decode()


@pytest.mark.specs
def test_put_database_count_error(monkeypatch, _clean_specs_table):
    """
    GIVEN body with invalid spec and spec id and database that raises DatabaseError
    WHEN put is called with the body and spec id
    THEN a 500 is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "1"
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
    spec_name = "id 1"
    user = "user 1"
    mock_database_check_would_exceed_free_tier = mock.MagicMock()
    mock_database_check_would_exceed_free_tier.side_effect = (
        package_database.exceptions.BaseError
    )
    monkeypatch.setattr(
        package_database.get(),
        "check_would_exceed_free_tier",
        mock_database_check_would_exceed_free_tier,
    )

    response = specs.put(body=body.encode(), spec_name=spec_name, user=user)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


@pytest.mark.specs
def test_put_storage_error(monkeypatch, _clean_specs_table):
    """
    GIVEN body with invalid spec and spec id
    WHEN put is called with the body and spec id
    THEN a 400 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "1"
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
    spec_name = "id 1"
    user = "user 1"
    mock_storage_create_update_spec = mock.MagicMock()
    mock_storage_create_update_spec.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(
        storage.get_storage_facade(),
        "create_update_spec",
        mock_storage_create_update_spec,
    )

    response = specs.put(body=body.encode(), spec_name=spec_name, user=user)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "storing" in response.data.decode()


@pytest.mark.specs
def test_put_database_update_error(monkeypatch, _clean_specs_table):
    """
    GIVEN body and spec id
    WHEN put is called with the body and spec id
    THEN the spec is stored against the spec id.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version = "1"
    spec = {
        "info": {"version": version},
        "components": {
            "schemas": {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            }
        },
    }
    body = json.dumps(spec)
    spec_name = "id 1"
    user = "user 1"
    mock_database_create_update_spec = mock.MagicMock()
    mock_database_create_update_spec.side_effect = package_database.exceptions.BaseError
    monkeypatch.setattr(
        package_database.get(),
        "create_update_spec",
        mock_database_create_update_spec,
    )

    response = specs.put(body=body.encode(), spec_name=spec_name, user=user)

    spec_str = storage.get_storage_facade().get_spec(
        user=user, name=spec_name, version=version
    )
    assert f'"{version}"' in spec_str
    assert '"Schema"' in spec_str
    assert '"x-tablename"' in spec_str
    assert '"schema"' in spec_str
    assert package_database.get().count_customer_models(sub=user) == 0
    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


@pytest.mark.specs
def test_delete(_clean_specs_table):
    """
    GIVEN database and storage with spec and user and spec id
    WHEN put is called with the body and spec id
    THEN the spec is deleted from the storage and database.
    """
    spec_name = "id 1"
    user = "user 1"
    version = "1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=1
    )
    storage.get_storage_facade().create_update_spec(
        user=user, name=spec_name, version=version, spec_str="spec str 1"
    )

    response = specs.delete(spec_name=spec_name, user=user)

    with pytest.raises(storage.exceptions.StorageError):
        storage.get_storage_facade().get_spec(
            user=user, name=spec_name, version=version
        )
    assert package_database.get().count_customer_models(sub=user) == 0
    assert response.status_code == 204


@pytest.mark.specs
def test_delete_database_error(monkeypatch, _clean_specs_table):
    """
    GIVEN database that raises a DatabaseError and storage with spec and user and spec
        id
    WHEN put is called with the body and spec id
    THEN the spec is deleted from the storage.
    """
    spec_name = "id 1"
    user = "user 1"
    version = "1"
    mock_database_delete_spec = mock.MagicMock()
    mock_database_delete_spec.side_effect = package_database.exceptions.BaseError
    monkeypatch.setattr(
        package_database.get(),
        "delete_spec",
        mock_database_delete_spec,
    )
    storage.get_storage_facade().create_update_spec(
        user=user, name=spec_name, version=version, spec_str="spec str 1"
    )

    response = specs.delete(spec_name=spec_name, user=user)

    with pytest.raises(storage.exceptions.StorageError):
        storage.get_storage_facade().get_spec(
            user=user, name=spec_name, version=version
        )
    assert response.status_code == 204


@pytest.mark.specs
def test_delete_storage_error(monkeypatch, _clean_specs_table):
    """
    GIVEN database and storage that raises a StorageError with spec and user and spec
        id
    WHEN put is called with the body and spec id
    THEN the spec is deleted from the database.
    """
    spec_name = "id 1"
    user = "user 1"
    version = "1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=1
    )
    mock_storage_delete_spec = mock.MagicMock()
    mock_storage_delete_spec.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(
        storage.get_storage_facade(),
        "delete_spec",
        mock_storage_delete_spec,
    )

    response = specs.delete(spec_name=spec_name, user=user)

    assert package_database.get().count_customer_models(sub=user) == 0
    assert response.status_code == 204

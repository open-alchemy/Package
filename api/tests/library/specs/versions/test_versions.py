"""Tests for the specs endpoint."""

import json
from unittest import mock

import pytest
from library.facades import server, storage
from library.specs import versions
from open_alchemy import package_database


@pytest.mark.specs_versions
def test_list_(_clean_specs_table):
    """
    GIVEN user, spec id and database with a single spec
    WHEN list_ is called with the user and spec id
    THEN the version of the spec is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    model_count = 1
    package_database.get().create_update_spec(
        sub=user, name=spec_name, version=version, model_count=model_count
    )

    response = versions.list_(user=user, spec_name=spec_name)

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


@pytest.mark.specs_versions
def test_list_not_found(_clean_specs_table):
    """
    GIVEN user, spec id and empty storage
    WHEN list_ is called with the user and spec id
    THEN 404 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"

    response = versions.list_(user=user, spec_name=spec_name)

    assert response.status_code == 404
    assert response.mimetype == "text/plain"
    assert spec_name in response.data.decode()


@pytest.mark.specs_versions
def test_list_database_error(monkeypatch):
    """
    GIVEN user, spec id and database that raises a databaseError
    WHEN list_ is called with the user and spec id
    THEN 500 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    mock_database_list_spec_versions = mock.MagicMock()
    mock_database_list_spec_versions.side_effect = package_database.exceptions.BaseError
    monkeypatch.setattr(
        package_database.get(),
        "list_spec_versions",
        mock_database_list_spec_versions,
    )

    response = versions.list_(user=user, spec_name=spec_name)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


@pytest.mark.specs_versions
def test_get():
    """
    GIVEN user and version and database and storage with a single spec
    WHEN get is called with the user and spec id
    THEN the spec value is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=user,
        name=spec_name,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )

    response = versions.get(user=user, spec_name=spec_name, version=version)

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert f"version: '{version}'" in response.data.decode()
    assert "key: value" in response.data.decode()


@pytest.mark.specs_versions
def test_get_storage_facade_error(monkeypatch):
    """
    GIVEN user and database with a spec but storage that raises an error
    WHEN get is called with the user and spec id
    THEN a 500 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"
    mock_storage_get_spec = mock.MagicMock()
    mock_storage_get_spec.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(storage.get_storage_facade(), "get_spec", mock_storage_get_spec)

    response = versions.get(user=user, spec_name=spec_name, version=version)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "reading" in response.data.decode()


@pytest.mark.specs_versions
def test_get_storage_facade_miss(_clean_specs_table):
    """
    GIVEN user and database with a spec but empty storage
    WHEN get is called with the user and spec id
    THEN a 404 is returned.
    """
    user = "user 1"
    spec_name = "spec name 1"
    version = "1"

    response = versions.get(user=user, spec_name=spec_name, version=version)

    assert response.status_code == 404
    assert response.mimetype == "text/plain"
    assert spec_name in response.data.decode()
    assert "not find" in response.data.decode()


@pytest.mark.specs_versions
def test_put(monkeypatch, _clean_specs_table):
    """
    GIVEN body, spec id, user and version
    WHEN put is called with the body, spec id, user and version
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

    response = versions.put(
        body=body.encode(), spec_name=spec_name, version=version, user=user
    )

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


@pytest.mark.specs_versions
def test_put_invalid_spec_error(monkeypatch):
    """
    GIVEN body with invalid spec, spec id, user and version
    WHEN put is called with the body, spec id, user and version
    THEN a 400 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    body = "body 1"
    spec_name = "id 1"
    user = "user 1"
    version = "1"

    response = versions.put(
        body=body.encode(), spec_name=spec_name, version=version, user=user
    )

    assert response.status_code == 400
    assert response.mimetype == "text/plain"
    assert "not valid" in response.data.decode()


@pytest.mark.specs_versions
def test_put_version_mismatch_error(monkeypatch):
    """
    GIVEN body, spec id, user and version different to that in the body
    WHEN put is called with the body, spec id, user and version
    THEN a 400 with an invalid spec is returned.
    """
    mock_request = mock.MagicMock()
    mock_headers = {"X-LANGUAGE": "JSON"}
    mock_request.headers = mock_headers
    monkeypatch.setattr(server.Request, "request", mock_request)
    version_1 = "1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    body = json.dumps(
        {"info": {"version": version_1}, "components": {"schemas": schemas}}
    )
    spec_name = "id 1"
    user = "user 1"
    version_2 = "version 2"

    response = versions.put(
        body=body.encode(), spec_name=spec_name, version=version_2, user=user
    )

    assert response.status_code == 400
    assert response.mimetype == "text/plain"
    assert version_1 in response.data.decode()
    assert version_2 in response.data.decode()


@pytest.mark.specs_versions
def test_put_too_many_models_error(monkeypatch, _clean_specs_table):
    """
    GIVEN body, spec id, version and user that already has too many models
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
    spec_name_1 = "id 1"
    user = "user 1"
    package_database.get().create_update_spec(
        sub=user, name=spec_name_1, version="1", model_count=100
    )

    spec_name_2 = "id 2"
    response = versions.put(
        body=body.encode(), spec_name=spec_name_2, version=version, user=user
    )

    assert response.status_code == 402
    assert response.mimetype == "text/plain"
    assert "exceeded" in response.data.decode()
    assert ": 100," in response.data.decode()
    assert "spec: 1" in response.data.decode()


@pytest.mark.specs_versions
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
    mock_database_count_customer_models = mock.MagicMock()
    mock_database_count_customer_models.side_effect = (
        package_database.exceptions.BaseError
    )
    monkeypatch.setattr(
        package_database.get(),
        "count_customer_models",
        mock_database_count_customer_models,
    )

    response = versions.put(
        body=body.encode(), spec_name=spec_name, version=version, user=user
    )

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "database" in response.data.decode()


@pytest.mark.specs_versions
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

    response = versions.put(
        body=body.encode(), spec_name=spec_name, version=version, user=user
    )

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "storing" in response.data.decode()


@pytest.mark.specs_versions
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

    response = versions.put(
        body=body.encode(), spec_name=spec_name, version=version, user=user
    )

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

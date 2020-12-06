"""Tests for the specs endpoint."""

import json
from unittest import mock

from library.specs import versions
from library.facades import storage, server, database


def test_list_():
    """
    GIVEN user, spec id and storage with a single spec
    WHEN list_ is called with the user and spec id
    THEN the version of the spec is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version = "version 1"
    storage.get_storage_facade().create_update_spec(
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
        storage.get_storage_facade(),
        "get_spec_versions",
        mock_storage_get_spec_versions,
    )

    response = versions.list_(user=user, spec_id=spec_id)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "storage" in response.data.decode()


def test_get():
    """
    GIVEN user and version and database and storage with a single spec
    WHEN get is called with the user and spec id
    THEN the spec value is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version = "version 1"
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=user,
        spec_id=spec_id,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )

    response = versions.get(user=user, spec_id=spec_id, version=version)

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert f"version: {version}" in response.data.decode()
    assert f"key: value" in response.data.decode()


def test_get_storage_facade_error(monkeypatch):
    """
    GIVEN user and database with a spec but storage that raises an error
    WHEN get is called with the user and spec id
    THEN a 500 is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version = "version 1"
    mock_storage_get_spec = mock.MagicMock()
    mock_storage_get_spec.side_effect = storage.exceptions.StorageError
    monkeypatch.setattr(storage.get_storage_facade(), "get_spec", mock_storage_get_spec)

    response = versions.get(user=user, spec_id=spec_id, version=version)

    assert response.status_code == 500
    assert response.mimetype == "text/plain"
    assert "reading" in response.data.decode()


def test_get_storage_facade_miss(_clean_package_storage_table):
    """
    GIVEN user and database with a spec but empty storage
    WHEN get is called with the user and spec id
    THEN a 404 is returned.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version = "version 1"

    response = versions.get(user=user, spec_id=spec_id, version=version)

    assert response.status_code == 404
    assert response.mimetype == "text/plain"
    assert spec_id in response.data.decode()
    assert "not find" in response.data.decode()


def test_put(monkeypatch, _clean_package_storage_table):
    """
    GIVEN body, spec id, user and version
    WHEN put is called with the body, spec id, user and version
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

    response = versions.put(
        body=body.encode(), spec_id=spec_id, version=version, user=user
    )

    assert storage.get_storage_facade().get_spec(
        user=user, spec_id=spec_id, version=version
    ) == json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))
    assert database.get_database().count_customer_models(sub=user) == 1
    assert response.status_code == 204


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
    spec_id = "id 1"
    user = "user 1"
    version = "version 1"

    response = versions.put(
        body=body.encode(), spec_id=spec_id, version=version, user=user
    )

    assert response.status_code == 400
    assert response.mimetype == "text/plain"
    assert "not valid" in response.data.decode()


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
    version_1 = "version 1"
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
    spec_id = "id 1"
    user = "user 1"
    version_2 = "version 2"

    response = versions.put(
        body=body.encode(), spec_id=spec_id, version=version_2, user=user
    )

    assert response.status_code == 400
    assert response.mimetype == "text/plain"
    assert version_1 in response.data.decode()
    assert version_2 in response.data.decode()


# def test_put_too_many_models_error(monkeypatch, _clean_package_storage_table):
#     """
#     GIVEN body spec and spec id and user that already has too many models
#     WHEN put is called with the body and spec id
#     THEN a 402 with an invalid spec is returned.
#     """
#     mock_request = mock.MagicMock()
#     mock_headers = {"X-LANGUAGE": "JSON"}
#     mock_request.headers = mock_headers
#     monkeypatch.setattr(server.Request, "request", mock_request)
#     version = "version 1"
#     schemas = {
#         "Schema": {
#             "type": "object",
#             "x-tablename": "schema",
#             "properties": {"id": {"type": "integer"}},
#         }
#     }
#     body = json.dumps(
#         {"info": {"version": version}, "components": {"schemas": schemas}}
#     )
#     spec_id = "id 1"
#     user = "user 1"
#     database.get_database().create_update_spec(
#         sub=user, spec_id=spec_id, version="version 1", model_count=100
#     )

#     response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

#     assert response.status_code == 402
#     assert response.mimetype == "text/plain"
#     assert "exceeded" in response.data.decode()
#     assert ": 100," in response.data.decode()
#     assert "spec: 1" in response.data.decode()


# def test_put_database_count_error(monkeypatch, _clean_package_storage_table):
#     """
#     GIVEN body with invalid spec and spec id and database that raises DatabaseError
#     WHEN put is called with the body and spec id
#     THEN a 500 is returned.
#     """
#     mock_request = mock.MagicMock()
#     mock_headers = {"X-LANGUAGE": "JSON"}
#     mock_request.headers = mock_headers
#     monkeypatch.setattr(server.Request, "request", mock_request)
#     version = "version 1"
#     schemas = {
#         "Schema": {
#             "type": "object",
#             "x-tablename": "schema",
#             "properties": {"id": {"type": "integer"}},
#         }
#     }
#     body = json.dumps(
#         {"info": {"version": version}, "components": {"schemas": schemas}}
#     )
#     spec_id = "id 1"
#     user = "user 1"
#     mock_database_count_customer_models = mock.MagicMock()
#     mock_database_count_customer_models.side_effect = database.exceptions.DatabaseError
#     monkeypatch.setattr(
#         database.get_database(),
#         "count_customer_models",
#         mock_database_count_customer_models,
#     )

#     response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

#     assert response.status_code == 500
#     assert response.mimetype == "text/plain"
#     assert "database" in response.data.decode()


# def test_put_storage_error(monkeypatch, _clean_package_storage_table):
#     """
#     GIVEN body with invalid spec and spec id
#     WHEN put is called with the body and spec id
#     THEN a 400 with an invalid spec is returned.
#     """
#     mock_request = mock.MagicMock()
#     mock_headers = {"X-LANGUAGE": "JSON"}
#     mock_request.headers = mock_headers
#     monkeypatch.setattr(server.Request, "request", mock_request)
#     version = "version 1"
#     schemas = {
#         "Schema": {
#             "type": "object",
#             "x-tablename": "schema",
#             "properties": {"id": {"type": "integer"}},
#         }
#     }
#     body = json.dumps(
#         {"info": {"version": version}, "components": {"schemas": schemas}}
#     )
#     spec_id = "id 1"
#     user = "user 1"
#     mock_storage_create_update_spec = mock.MagicMock()
#     mock_storage_create_update_spec.side_effect = storage.exceptions.StorageError
#     monkeypatch.setattr(
#         storage.get_storage_facade(),
#         "create_update_spec",
#         mock_storage_create_update_spec,
#     )

#     response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

#     assert response.status_code == 500
#     assert response.mimetype == "text/plain"
#     assert "storing" in response.data.decode()


# def test_put_database_update_error(monkeypatch, _clean_package_storage_table):
#     """
#     GIVEN body and spec id
#     WHEN put is called with the body and spec id
#     THEN the spec is stored against the spec id.
#     """
#     mock_request = mock.MagicMock()
#     mock_headers = {"X-LANGUAGE": "JSON"}
#     mock_request.headers = mock_headers
#     monkeypatch.setattr(server.Request, "request", mock_request)
#     version = "version 1"
#     schemas = {
#         "Schema": {
#             "type": "object",
#             "x-tablename": "schema",
#             "properties": {"id": {"type": "integer"}},
#         }
#     }
#     body = json.dumps(
#         {"info": {"version": version}, "components": {"schemas": schemas}}
#     )
#     spec_id = "id 1"
#     user = "user 1"
#     mock_database_create_update_spec = mock.MagicMock()
#     mock_database_create_update_spec.side_effect = database.exceptions.DatabaseError
#     monkeypatch.setattr(
#         database.get_database(),
#         "create_update_spec",
#         mock_database_create_update_spec,
#     )

#     response = specs.put(body=body.encode(), spec_id=spec_id, user=user)

#     assert storage.get_storage_facade().get_spec(
#         user=user, spec_id=spec_id, version=version
#     ) == json.dumps({"components": {"schemas": schemas}}, separators=(",", ":"))
#     assert database.get_database().count_customer_models(sub=user) == 0
#     assert response.status_code == 500
#     assert response.mimetype == "text/plain"
#     assert "database" in response.data.decode()

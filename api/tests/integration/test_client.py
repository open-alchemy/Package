"""Tests for spec controller."""

import json

import jwt
import pytest
from library import config
from library.facades import storage
from open_alchemy import package_database

OPTIONS_TESTS = [
    pytest.param("/v1/specs/spec1", "PUT", id="/v1/specs/{spec-id}"),
]


@pytest.mark.parametrize("path, method", OPTIONS_TESTS)
def test_endpoint_options(client, path, method):
    """
    GIVEN path and method
    WHEN OPTIONS {path} is called with the CORS Method and X-LANGUAGE Headers
    THEN Access-Control-Allow-Headers is returned with x-language.
    """
    response = client.options(
        path,
        headers={
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "x-language",
        },
    )

    assert "Access-Control-Allow-Headers" in response.headers
    assert (
        response.headers["Access-Control-Allow-Headers"]
        == config.get_env().access_control_allow_headers
    )


@pytest.mark.parametrize(
    "url",
    [
        "/v1/specs",
        "/v1/specs/spec 1",
        "/v1/specs/spec 1/versions",
        "/v1/specs/spec 1/versions/version 1",
    ],
)
def test_get_unauthorized(client, url):
    """
    GIVEN url and data
    WHEN GET url is called without the Authorization header
    THEN 401 is returned.
    """
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.parametrize("url", ["/v1/specs/spec 1"])
def test_delete_unauthorized(client, url):
    """
    GIVEN url and data
    WHEN DELETE url is called without the Authorization header
    THEN 401 is returned.
    """
    response = client.delete(url)

    assert response.status_code == 401


@pytest.mark.parametrize(
    "url", ["/v1/specs/spec 1", "/v1/specs/spec 1/versions/version 1"]
)
def test_put_unauthorized(client, url):
    """
    GIVEN url and data
    WHEN PUT url is called without the Authorization header
    THEN 401 is returned.
    """
    data = "spec 1"

    response = client.put(url, data=data)

    assert response.status_code == 401


def test_specs_get(client, _clean_spec_table):
    """
    GIVEN database with a single spec
    WHEN GET /v1/specs is called with the Authorization header
    THEN the spec id is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    model_count = 1
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version, model_count=model_count
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get("/v1/specs", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    spec_infos = json.loads(response.data.decode())
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["spec_id"] == spec_id
    assert spec_info["version"] == version
    assert spec_info["model_count"] == model_count
    assert "updated_at" in spec_info


def test_specs_spec_id_get(client, _clean_spec_table):
    """
    GIVEN database and storage with a single spec
    WHEN GET /v1/specs/{spec_id} is called with the Authorization header
    THEN the spec is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version, model_count=1
    )
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        spec_id=spec_id,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/specs/{spec_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert "key: value" in response.data.decode()


def test_specs_spec_id_put(client, _clean_spec_table):
    """
    GIVEN spec id, data and token
    WHEN PUT /v1/specs/{spec-id} is called with the Authorization header
    THEN the value is stored and written to the database against the spec id.
    """
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    data = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.put(
        f"/v1/specs/{spec_id}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert '"x-tablename":"schema"' in storage.get_storage_facade().get_spec(
        user=sub, spec_id=spec_id, version=version
    )


def test_specs_spec_id_delete(client, _clean_spec_table):
    """
    GIVEN database and storage with a single spec
    WHEN DELETE /v1/specs/{spec_id} is called with the Authorization header
    THEN the spec is deleted from the database and storage.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version, model_count=1
    )
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        spec_id=spec_id,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.delete(
        f"/v1/specs/{spec_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    with pytest.raises(storage.exceptions.StorageError):
        storage.get_storage_facade().get_spec(
            user=sub, spec_id=spec_id, version=version
        )
    assert package_database.get().count_customer_models(sub=sub) == 0


def test_specs_spec_id_versions_get(client, _clean_spec_table):
    """
    GIVEN database and storage with a single spec
    WHEN GET /v1/specs/{spec_id}/versions is called with the Authorization header
    THEN the version is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    model_count = 1
    package_database.get().create_update_spec(
        sub=sub, id_=spec_id, version=version, model_count=model_count
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/specs/{spec_id}/versions", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    spec_infos = json.loads(response.data.decode())
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["spec_id"] == spec_id
    assert spec_info["version"] == version
    assert spec_info["model_count"] == model_count
    assert "updated_at" in spec_info


def test_specs_spec_id_version_version_get(client):
    """
    GIVEN storage with a single spec
    WHEN GET /v1/specs/{spec_id}/versions/{version} is called with the Authorization
        header
    THEN the spec is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        spec_id=spec_id,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/specs/{spec_id}/versions/{version}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert "key: value" in response.data.decode()


def test_specs_spec_id_versions_version_put(client, _clean_spec_table):
    """
    GIVEN spec id, data, version and token
    WHEN PUT /v1/specs/{spec-id}/versions/{version} is called with the Authorization
        header
    THEN the value is stored and written to the database against the spec id.
    """
    version = "version 1"
    schemas = {
        "Schema": {
            "type": "object",
            "x-tablename": "schema",
            "properties": {"id": {"type": "integer"}},
        }
    }
    data = json.dumps(
        {"info": {"version": version}, "components": {"schemas": schemas}}
    )
    spec_id = "id 1"
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.put(
        f"/v1/specs/{spec_id}/versions/{version}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert '"x-tablename":"schema"' in storage.get_storage_facade().get_spec(
        user=sub, spec_id=spec_id, version=version
    )

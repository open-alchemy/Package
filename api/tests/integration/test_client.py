"""Tests for spec controller."""

import json

import jwt
import pytest
from library import config
from library.facades import storage
from open_alchemy import package_database

OPTIONS_TESTS = [
    pytest.param("/v1/specs/spec1", "PUT", id="/v1/specs/{spec_name}"),
]


@pytest.mark.parametrize("path, method", OPTIONS_TESTS)
@pytest.mark.integration
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
        == config.get().access_control_allow_headers
    )


@pytest.mark.parametrize(
    "url",
    [
        "/v1/specs",
        "/v1/specs/spec1",
        "/v1/specs/spec1/versions",
        "/v1/specs/spec1/versions/1",
        "/v1/credentials/default",
    ],
)
@pytest.mark.integration
def test_get_unauthorized(client, url):
    """
    GIVEN url and data
    WHEN GET url is called without the Authorization header
    THEN 401 is returned.
    """
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.parametrize("url", ["/v1/specs/spec1"])
@pytest.mark.integration
def test_delete_unauthorized(client, url):
    """
    GIVEN url and data
    WHEN DELETE url is called without the Authorization header
    THEN 401 is returned.
    """
    response = client.delete(url)

    assert response.status_code == 401


@pytest.mark.parametrize("url", ["/v1/specs/spec1", "/v1/specs/spec1/versions/1"])
@pytest.mark.integration
def test_put_unauthorized(client, url):
    """
    GIVEN url and data
    WHEN PUT url is called without the Authorization header
    THEN 401 is returned.
    """
    data = "spec 1"

    response = client.put(url, data=data)

    assert response.status_code == 401


@pytest.mark.integration
def test_specs_get(client, _clean_specs_table):
    """
    GIVEN database with a single spec
    WHEN GET /v1/specs is called with the Authorization header
    THEN the spec name is returned.
    """
    sub = "sub 1"
    spec_name = "spec1"
    version = "1"
    model_count = 1
    package_database.get().create_update_spec(
        sub=sub, name=spec_name, version=version, model_count=model_count
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get("/v1/specs", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    spec_infos = json.loads(response.data.decode())
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["name"] == spec_name
    assert spec_info["id"] == spec_name
    assert spec_info["version"] == version
    assert spec_info["model_count"] == model_count
    assert "updated_at" in spec_info


@pytest.mark.integration
def test_specs_spec_name_get(client, _clean_specs_table):
    """
    GIVEN database and storage with a single spec
    WHEN GET /v1/specs/{spec_name} is called with the Authorization header
    THEN the spec is returned.
    """
    sub = "sub 1"
    spec_name = "spec1"
    version = "1"
    package_database.get().create_update_spec(
        sub=sub, name=spec_name, version=version, model_count=1
    )
    spec = {"components": {}}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        name=spec_name,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/specs/{spec_name}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    response_json = json.loads(response.data.decode())
    assert "components: {}" in response_json["value"]
    assert response_json["name"] == spec_name
    assert response_json["version"] == version


@pytest.mark.integration
def test_specs_spec_name_put_invalid_name(client):
    """
    GIVEN invalid spec name, data and token
    WHEN PUT /v1/specs/{spec_name} is called with the Authorization header
    THEN 400 is returned.
    """
    data = "data 1"
    spec_name = "spec 1"
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.put(
        f"/v1/specs/{spec_name}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_specs_spec_name_put(client, _clean_specs_table):
    """
    GIVEN spec id, data and token
    WHEN PUT /v1/specs/{spec_name} is called with the Authorization header
    THEN the value is stored and written to the database against the spec id.
    """
    version = "1"
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
    spec_name = "spec1"
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.put(
        f"/v1/specs/{spec_name}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    assert '"x-tablename":"schema"' in storage.get_storage_facade().get_spec(
        user=sub, name=spec_name, version=version
    )


@pytest.mark.integration
def test_specs_spec_name_delete(client, _clean_specs_table):
    """
    GIVEN database and storage with a single spec
    WHEN DELETE /v1/specs/{spec_name} is called with the Authorization header
    THEN the spec is deleted from the database and storage.
    """
    sub = "sub 1"
    spec_name = "spe1"
    version = "1"
    package_database.get().create_update_spec(
        sub=sub, name=spec_name, version=version, model_count=1
    )
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        name=spec_name,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.delete(
        f"/v1/specs/{spec_name}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    with pytest.raises(storage.exceptions.StorageError):
        storage.get_storage_facade().get_spec(user=sub, name=spec_name, version=version)
    assert package_database.get().count_customer_models(sub=sub) == 0


@pytest.mark.integration
def test_specs_spec_name_versions_get(client, _clean_specs_table):
    """
    GIVEN database and storage with a single spec
    WHEN GET /v1/specs/{spec_name}/versions is called with the Authorization header
    THEN the version is returned.
    """
    sub = "sub 1"
    spec_name = "spec1"
    version = "1"
    model_count = 1
    package_database.get().create_update_spec(
        sub=sub, name=spec_name, version=version, model_count=model_count
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/specs/{spec_name}/versions", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    spec_infos = json.loads(response.data.decode())
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["name"] == spec_name
    assert spec_info["id"] == spec_name
    assert spec_info["version"] == version
    assert spec_info["model_count"] == model_count
    assert "updated_at" in spec_info


@pytest.mark.integration
def test_specs_spec_name_version_version_get(client, _clean_specs_table):
    """
    GIVEN storage with a single spec
    WHEN GET /v1/specs/{spec_name}/versions/{version} is called with the Authorization
        header
    THEN the spec is returned.
    """
    sub = "sub 1"
    spec_name = "spec1"
    version = "1"
    spec = {"components": {}}
    package_database.get().create_update_spec(
        sub=sub, name=spec_name, version=version, model_count=1
    )
    storage.get_storage_facade().create_update_spec(
        user=sub,
        name=spec_name,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/specs/{spec_name}/versions/{version}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    response_json = json.loads(response.data.decode())
    assert "components: {}" in response_json["value"]
    assert response_json["name"] == spec_name
    assert response_json["version"] == version


@pytest.mark.integration
def test_specs_spec_name_versions_version_put_invalid_version(client):
    """
    GIVEN spec id, data, invalid version and token
    WHEN PUT /v1/specs/{spec_name}/versions/{version} is called with the Authorization
        header
    THEN 400 is returned.
    """
    version = "a"
    data = "data 1"
    spec_name = "spec1"
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.put(
        f"/v1/specs/{spec_name}/versions/{version}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_specs_spec_name_versions_version_put(client, _clean_specs_table):
    """
    GIVEN spec id, data, version and token
    WHEN PUT /v1/specs/{spec_name}/versions/{version} is called with the Authorization
        header
    THEN the value is stored and written to the database against the spec id.
    """
    version = "1"
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
    spec_name = "spec1"
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.put(
        f"/v1/specs/{spec_name}/versions/{version}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    assert '"x-tablename":"schema"' in storage.get_storage_facade().get_spec(
        user=sub, name=spec_name, version=version
    )


@pytest.mark.integration
def test_credentials_default_get(client, _clean_credentials_table):
    """
    GIVEN
    WHEN GET /v1/credentials/default is called with the Authorization header
    THEN credentials are returned.
    """
    sub = "sub 1"
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.get(
        f"/v1/credentials/{config.get().default_credentials_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    response_data = json.loads(response.data.decode())
    assert "public_key" in response_data
    assert "secret_key" in response_data


@pytest.mark.integration
def test_credentials_default_delete(client, _clean_credentials_table):
    """
    GIVEN database with credentials
    WHEN DELETE /v1/credentials/default is called with the Authorization header
    THEN the credentials are deleted.
    """
    sub = "sub 1"
    package_database.get().create_update_credentials(
        sub=sub,
        id_=config.get().default_credentials_id,
        public_key="public key 1",
        secret_key_hash=b"secret key hash 1",
        salt=b"salt 1",
    )
    token = jwt.encode({"sub": sub}, "secret 1")

    response = client.delete(
        f"/v1/credentials/{config.get().default_credentials_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204
    assert "Access-Control-Allow-Origin" in response.headers
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == config.get().access_control_allow_origin
    )

    assert (
        package_database.get().get_credentials(
            sub=sub, id_=config.get().default_credentials_id
        )
        is None
    )

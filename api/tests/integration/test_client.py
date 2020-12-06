"""Tests for spec controller."""

import json

import jwt
import pytest
from library import config
from library.facades import storage, database

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
    respose = client.options(
        path,
        headers={
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "x-language",
        },
    )

    assert "Access-Control-Allow-Headers" in respose.headers
    assert (
        respose.headers["Access-Control-Allow-Headers"]
        == config.get_env().access_control_allow_headers
    )


def test_specs_put_unauthorized(client):
    """
    GIVEN spec id and data
    WHEN PUT /v1/specs/{spec-id} is called without the Authorization header
    THEN 401 is returned.
    """
    data = "spec 1"
    spec_id = "id 1"

    respose = client.put(f"/v1/specs/{spec_id}", data=data)

    assert respose.status_code == 401


def test_specs_get(client, _clean_package_storage_table):
    """
    GIVEN database with a single spec
    WHEN GET /v1/specs is called with the Authorization header
    THEN the spec id is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    database.get_database().create_update_spec(
        sub=sub, spec_id=spec_id, version="version 1", model_count=1
    )
    token = jwt.encode({"sub": sub}, "secret 1").decode()

    respose = client.get("/v1/specs", headers={"Authorization": f"Bearer {token}"})

    assert respose.status_code == 200
    assert "Access-Control-Allow-Origin" in respose.headers
    assert (
        respose.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert json.loads(respose.data.decode()) == [spec_id]


def test_specs_spec_id_get(client, _clean_package_storage_table):
    """
    GIVEN database and storage with a single spec
    WHEN GET /v1/specs/{spec_id} is called with the Authorization header
    THEN the spec is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    database.get_database().create_update_spec(
        sub=sub, spec_id=spec_id, version=version, model_count=1
    )
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        spec_id=spec_id,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1").decode()

    respose = client.get(
        f"/v1/specs/{spec_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert respose.status_code == 200
    assert "Access-Control-Allow-Origin" in respose.headers
    assert (
        respose.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert "key: value" in respose.data.decode()


def test_specs_spec_id_put(client, _clean_package_storage_table):
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
    token = jwt.encode({"sub": sub}, "secret 1").decode()

    respose = client.put(
        f"/v1/specs/{spec_id}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "X-LANGUAGE": "JSON"},
    )

    assert respose.status_code == 204
    assert "Access-Control-Allow-Origin" in respose.headers
    assert (
        respose.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    assert '"x-tablename":"schema"' in storage.get_storage_facade().get_spec(
        user=sub, spec_id=spec_id, version=version
    )


def test_specs_spec_id_delete(client, _clean_package_storage_table):
    """
    GIVEN database and storage with a single spec
    WHEN DELETE /v1/specs/{spec_id} is called with the Authorization header
    THEN the spec is deleted from the database and storage.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    database.get_database().create_update_spec(
        sub=sub, spec_id=spec_id, version=version, model_count=1
    )
    spec = {"key": "value"}
    storage.get_storage_facade().create_update_spec(
        user=sub,
        spec_id=spec_id,
        version=version,
        spec_str=json.dumps(spec, separators=(",", ":")),
    )
    token = jwt.encode({"sub": sub}, "secret 1").decode()

    respose = client.delete(
        f"/v1/specs/{spec_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert respose.status_code == 204
    assert "Access-Control-Allow-Origin" in respose.headers
    assert (
        respose.headers["Access-Control-Allow-Origin"]
        == config.get_env().access_control_allow_origin
    )

    with pytest.raises(storage.exceptions.StorageError):
        storage.get_storage_facade().get_spec(
            user=sub, spec_id=spec_id, version=version
        )
    assert database.get_database().count_customer_models(sub=sub) == 0

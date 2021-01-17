"""Tests for the helpers."""

import json

import pytest
import yaml
from library import exceptions
from library.helpers import spec

LOAD_ERROR_TESTS = [
    pytest.param(
        "INVALID",
        "",
        exceptions.LoadSpecError,
        "unsupported language INVALID, supported languages are JSON and YAML",
        id="invalid language",
    ),
    pytest.param(
        "JSON",
        "invalid JSON",
        exceptions.LoadSpecError,
        "body must be valid JSON",
        id="invalid JSON",
    ),
    pytest.param(
        "YAML",
        "not: valid: YAML",
        exceptions.LoadSpecError,
        "body must be valid YAML",
        id="invalid YAML schema",
    ),
    pytest.param(
        "YAML",
        ":",
        exceptions.LoadSpecError,
        "body must be valid YAML",
        id="invalid YAML value",
    ),
]


@pytest.mark.parametrize(
    "language, spec_str, expected_exception, expected_reason", LOAD_ERROR_TESTS
)
@pytest.mark.helpers
def test_load_error(language, spec_str, expected_exception, expected_reason):
    """
    GIVEN language and spec string
    WHEN load is called with the language and spec string
    THEN the expected exception is raised with the expected reason.
    """
    with pytest.raises(expected_exception) as exc:
        spec.load(spec_str=spec_str, language=language)

    assert str(exc.value) == expected_reason


LOAD_TESTS = [
    pytest.param(
        "JSON",
        '{"key": "value"}',
        id="JSON",
    ),
    pytest.param(
        "YAML",
        "key: value",
        id="YAML",
    ),
]


@pytest.mark.parametrize("language, spec_str", LOAD_TESTS)
@pytest.mark.helpers
def test_load(language, spec_str):
    """
    GIVEN language and spec string
    WHEN load is called with the language and spec string
    THEN the expected spec is returned.
    """
    returned_spec = spec.load(spec_str=spec_str, language=language)

    assert returned_spec == {"key": "value"}


CALC_VERSION_TESTS = [
    pytest.param("1", "1", id="number"),
    pytest.param("french toast", "440005914211", id="non sense value"),
    pytest.param(" 1", "1", id="whitespace padded number"),
    pytest.param("a", "97", id="character"),
    pytest.param("aaaaa", "418245599585", id="max length string"),
    pytest.param("aaaaaa", "418245599585", id="loner than max length string"),
]


@pytest.mark.parametrize("value, expected_result", CALC_VERSION_TESTS)
@pytest.mark.helpers
@pytest.mark.helpers
def test_calc_version(value, expected_result):
    """
    GIVEN version
    WHEN calc_version is called with the version
    THEN the expected result is returned.
    """
    returned_result = spec.calc_version(value)

    assert returned_result == expected_result


@pytest.mark.helpers
def test_process_invalid_str():
    """
    GIVEN invalid spec string
    WHEN process is called
    THEN LoadSpecError is raised.
    """
    with pytest.raises(exceptions.LoadSpecError) as exc:
        spec.process(spec_str="", language="INVAID")

    assert "INVAID" in str(exc)


@pytest.mark.helpers
def test_process_invalid_schemas():
    """
    GIVEN spec string
    WHEN process is called
    THEN LoadSpecError is raised.
    """
    with pytest.raises(exceptions.LoadSpecError) as exc:
        spec.process(spec_str=json.dumps({}), language="JSON")

    assert "not valid" in str(exc)


@pytest.mark.helpers
def test_process():
    """
    GIVEN spec string
    WHEN process is called
    THEN the version is calculated and the final string is returned.
    """
    version = "version 1"
    title = "title 1"
    description = "description 1"
    spec_dict = {
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
    spec_str = json.dumps(spec_dict)

    returned_result = spec.process(spec_str=spec_str, language="JSON")

    assert returned_result.version == "508508140393"
    assert returned_result.title == title
    assert returned_result.description == description
    assert f'"{version}"' in returned_result.spec_str
    assert '"Schema"' in returned_result.spec_str
    assert '"x-tablename"' in returned_result.spec_str
    assert '"schema"' in returned_result.spec_str
    assert returned_result.model_count == 1


@pytest.mark.parametrize(
    "schemas, expected_model_count",
    [
        pytest.param(
            {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                }
            },
            1,
            id="single x-tablename",
        ),
        pytest.param(
            {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                },
                "ChildSchema": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Schema"},
                        {
                            "type": "object",
                            "x-inherits": True,
                            "properties": {"child_id": {"type": "integer"}},
                        },
                    ]
                },
            },
            1,
            id="single x-inherits",
        ),
        pytest.param(
            {
                "Schema1": {
                    "type": "object",
                    "x-tablename": "schema_1",
                    "properties": {"id": {"type": "integer"}},
                },
                "Schema2": {
                    "type": "object",
                    "x-tablename": "schema_2",
                    "properties": {"id": {"type": "integer"}},
                },
            },
            2,
            id="multiple x-tablename",
        ),
        pytest.param(
            {
                "Schema": {
                    "type": "object",
                    "x-tablename": "schema",
                    "properties": {"id": {"type": "integer"}},
                },
                "ChildSchema1": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Schema"},
                        {
                            "type": "object",
                            "x-inherits": True,
                            "properties": {"child_id": {"type": "integer"}},
                        },
                    ]
                },
                "ChildSchema2": {
                    "allOf": [
                        {"$ref": "#/components/schemas/Schema"},
                        {
                            "type": "object",
                            "x-inherits": True,
                            "properties": {"child_id": {"type": "integer"}},
                        },
                    ]
                },
            },
            1,
            id="multiple x-inherits",
        ),
    ],
)
@pytest.mark.helpers
def test_process_model_count(schemas, expected_model_count):
    """
    GIVEN schemas
    WHEN process is called with the schemas
    THEN the expected model count is returned.
    """
    spec_str = json.dumps({"components": {"schemas": schemas}})

    returned_result = spec.process(spec_str=spec_str, language="JSON")

    assert returned_result.model_count == expected_model_count


@pytest.mark.parametrize(
    "version, spec_dict, expected_version",
    [
        pytest.param(
            "version 1",
            {"components": {"schemas": {"Schema": {"key": "value"}}}},
            "version 1",
            id="no info",
        ),
        pytest.param(
            "version 1",
            {"info": {}, "components": {"schemas": {"Schema": {"key": "value"}}}},
            "version 1",
            id="with info no version",
        ),
        pytest.param(
            "version 1",
            {
                "info": {"version": "version 2"},
                "components": {"schemas": {"Schema": {"key": "value"}}},
            },
            "version 2",
            id="with info with version",
        ),
    ],
)
@pytest.mark.helpers
def test_prepare(version, spec_dict, expected_version):
    """
    GIVEN spec string and version
    WHEN prepare is called with the spec and version
    THEN a nicely formatted spec is returned.
    """
    spec_str = json.dumps(spec_dict, separators=(",", ":"))

    returned_spec_str = spec.prepare(spec_str=spec_str, version=version)

    assert yaml.dump({"components": spec_dict["components"]}) in returned_spec_str
    assert expected_version in returned_spec_str
    assert returned_spec_str.count("info:") == 1

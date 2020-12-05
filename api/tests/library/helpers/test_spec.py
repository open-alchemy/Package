"""Tests for the helpers."""

import pytest
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
def test_load(language, spec_str):
    """
    GIVEN language and spec string
    WHEN load is called with the language and spec string
    THEN the expected exception spec is returned.
    """
    returned_spec = spec.load(spec_str=spec_str, language=language)

    assert returned_spec == {"key": "value"}


def test_dump():
    """
    GIVEN spec
    WHEN dump si called
    THEN the serialized spec is returned.
    """
    spec_ = {"key": "value"}

    returned_spec_str = spec.dump(spec=spec_)

    assert returned_spec_str == '{"key": "value"}'

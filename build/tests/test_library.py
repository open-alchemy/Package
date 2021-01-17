"""Tests for the library."""

import json
import typing

import library
import pytest


def test_parse_spec_storage_location():
    """
    GIVEN spec storage location
    WHEN parse_spec_storage_location is called
    THEN the sub, spec id and version is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    spec_storage_location = f"{sub}/{spec_id}/{version}-spec.json"

    returned_location = library.parse_spec_storage_location(spec_storage_location)

    assert returned_location.sub == sub
    assert returned_location.spec_id == spec_id
    assert returned_location.version == version


@pytest.mark.parametrize(
    "spec_id, expected_package_name",
    [
        pytest.param("test", "test", id="no -"),
        pytest.param("test-name", "test_name", id="single -"),
        pytest.param("the-test-name", "the_test_name", id="multiple -"),
    ],
)
def test_calclate_package_name(spec_id, expected_package_name):
    """
    GIVEN storage location
    WHEN calclate_package_name is called with the storage location
    THEN the expected name is returned.
    """
    storage_location = library.SpecStorageLocation(
        sub="user 1", spec_id=spec_id, version="version 1"
    )

    returned_package_name = library.calclate_package_name(
        storage_location=storage_location
    )

    assert returned_package_name == expected_package_name


def test_generate(tmp_path):
    """
    GIVEN spec storage location and spec path
    WHEN generate is called
    THEN 2 packages are created with the spected storage locations.
    """
    sub = "sub 1"
    spec_id = "spec-id-1"
    version = "version1"
    spec_storage_location = f"{sub}/{spec_id}/{version}-spec.json"

    spec_path = tmp_path / "spec.json"
    spec_path.write_text(
        json.dumps(
            {
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
        )
    )

    returned_packages = library.generate(spec_storage_location, spec_path)

    assert len(returned_packages) == 1
    seen_suffixes: typing.Set[str] = set()
    for package in returned_packages[:1]:
        assert package.path.exists()
        assert str(package.path).startswith(str(tmp_path))
        assert "spec.json" not in str(package.path)

        assert package.storage_location.startswith(f"{sub}/{spec_id}/")
        assert version in package.storage_location
        assert spec_id.replace("-", "_") in package.storage_location

        assert package.storage_location.endswith(package.path.suffix)

        assert package.path.suffix not in seen_suffixes
        seen_suffixes.add(package.path.suffix)

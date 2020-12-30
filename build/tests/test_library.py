"""Tests for the library."""

import json
import typing

import library


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


def test_generate(tmp_path):
    """
    GIVEN spec storage location and spec path
    WHEN generate is called
    THEN 2 packages are created with the spected storage locations.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
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

    assert len(returned_packages) == 2
    seen_suffixes: typing.Set[str] = set()
    for package in returned_packages:
        assert package.path.exists()
        assert str(package.path).startswith(str(tmp_path))
        assert "spec.json" not in str(package.path)

        assert package.storage_location.startswith(f"{sub}/{spec_id}/")
        assert version in package.storage_location

        assert package.storage_location.endswith(package.path.suffix)

        assert package.path.suffix not in seen_suffixes
        seen_suffixes.add(package.path.suffix)

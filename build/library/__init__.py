"""Library for app."""

import dataclasses
import pathlib
import typing

import open_alchemy


@dataclasses.dataclass
class SpecStorageLocation:
    """
    The location of a spec in storage.

    Attrs:
        sub: Unique identifier for the user
        spec_id: Unique identifier for the spec
        version: The version of the spec

    """

    sub: str
    spec_id: str
    version: str


def parse_spec_storage_location(location: str) -> SpecStorageLocation:
    """
    Parse the spec storage location into components.

    Args:
        location: The spec storage location to parse.

    Returns:
        The parsed spec storage location.

    """
    sub, spec_id, filename = location.split("/")
    version = filename[: -len("-spec.json")]
    return SpecStorageLocation(sub, spec_id, version)


@dataclasses.dataclass
class Package:
    """
    Information about a generated package.

    Attrs:
        storage_location: The location where the package needs to be stored
        path: The path where the package can be read from the local disk

    """

    storage_location: str
    path: pathlib.Path


PackageList = typing.List[Package]


def generate(spec_storage_location: str, spec_path: pathlib.Path) -> PackageList:
    """
    Generate the package for the spec.

    Args:
        spec_storage_location: The location of the spec in storage.
        spec_path: The local path to the spec file.

    Returns:
        A list of generated packages.

    """
    location = parse_spec_storage_location(spec_storage_location)
    dist_path = spec_path.parent

    open_alchemy.build_json(
        spec_path,
        location.spec_id,
        str(dist_path),
        open_alchemy.PackageFormat.SDIST | open_alchemy.PackageFormat.WHEEL,
    )

    tar_gz_path = next(dist_path.glob("**/*.tar.gz"))
    tar_gz_storage_location = f"{location.sub}/{location.spec_id}/{tar_gz_path.name}"
    tar_gz_package = Package(storage_location=tar_gz_storage_location, path=tar_gz_path)

    wheel_path = next(dist_path.glob("**/*.whl"))
    wheel_storage_location = f"{location.sub}/{location.spec_id}/{wheel_path.name}"
    wheel_package = Package(storage_location=wheel_storage_location, path=wheel_path)

    return [tar_gz_package, wheel_package]

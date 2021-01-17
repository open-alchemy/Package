"""Helpers for spec."""

import dataclasses
import json
import typing

import open_alchemy
import yaml
from open_alchemy import build
from packaging import version as packaging_version
from yaml import parser, scanner

from .. import exceptions, types

TSpec = typing.Dict[str, typing.Any]


def load(*, spec_str: str, language: str) -> TSpec:
    """
    Load the spec from a string using a particular language.

    Raises LoadSpecError if loading the spec fails.

    Args:
        spec_str: The string of the spec.
        language: The language to use for loading.

    Returns:
        The loaded spec.

    """
    if language == "YAML":
        try:
            return yaml.safe_load(spec_str)
        except (parser.ParserError, scanner.ScannerError) as exc:
            raise exceptions.LoadSpecError("body must be valid YAML") from exc
    elif language == "JSON":
        try:
            return json.loads(spec_str)
        except json.JSONDecodeError as exc:
            raise exceptions.LoadSpecError("body must be valid JSON") from exc

    raise exceptions.LoadSpecError(
        f"unsupported language {language}, supported languages are JSON and YAML"
    )


@dataclasses.dataclass
class TSpecInfo:
    """
    Key information about a spec.

    Attrs:
        spec_str:  The spec in string format
        version:  The version of the spec
        title:  The title of the spec
        description:  The description of the spec
        model_count:  The number of models in the spec

    """

    spec_str: types.TSpecValue
    version: types.TSpecVersion
    title: types.TSpecOptTitle
    description: types.TSpecOptDescription
    model_count: types.TSpecModelCount


def calc_version(value: types.TSpecVersion) -> str:
    """
    Validate the version.

    Args:
        value: The version to validate.

    Returns:
        Whether the version is valid.

    """
    try:
        return packaging_version.Version(value).public
    except packaging_version.InvalidVersion:
        return str(int.from_bytes(value[0:5].encode(), "big"))


def process(*, spec_str: str, language: str) -> TSpecInfo:
    """
    Check that the spec is valid and calculates the version.

    Args:
        spec_str: The string to process.
        language: The language of the spec, either YAML or JSON.

    """
    spec = load(spec_str=spec_str, language=language)
    try:
        schemas = build.get_schemas(spec=spec)
    except open_alchemy.exceptions.MalformedSchemaError as exc:
        raise exceptions.LoadSpecError(f"the schema is not valid, {exc}") from exc
    spec_info = build.calculate_spec_info(schemas=schemas, spec=spec)

    version = calc_version(spec_info.version)

    model_count = spec_info.spec_str.count('"x-tablename":')

    return TSpecInfo(
        spec_str=spec_info.spec_str,
        version=version,
        title=spec_info.title,
        description=spec_info.description,
        model_count=model_count,
    )


def prepare(*, spec_str: str, version: str) -> str:
    """
    Prepare a stored spec to be returned to the user.

    De-serializes using JSON, adds version and serializes using YAML.

    Args:
        spec_str: The spec as it is stored.
        version: The version of the spec.

    Returns:
        The spec in a user friendly form.

    """
    spec = json.loads(spec_str)
    info = {"version": version}
    if "info" in spec:
        info = {**info, **spec["info"]}
    components = spec["components"]
    return yaml.dump({"info": info}) + yaml.dump({"components": components})

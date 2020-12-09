"""Helpers for spec."""

import dataclasses
import json
import typing

from open_alchemy import build
import open_alchemy
import yaml
from yaml import parser
from yaml import scanner

from .. import exceptions


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
    """Key information about a spec."""

    # The spec in string format
    spec_str: str
    # The version of the spec
    version: str
    # The number of models in the spec
    model_count: int


def process(*, spec_str: str, language: str) -> TSpecInfo:
    """
    Checks that the spec is valid and calculates the version.

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

    model_count = spec_info.spec_str.count('"x-tablename":') + spec_info.spec_str.count(
        '"x-inherits":'
    )

    return TSpecInfo(
        spec_str=spec_info.spec_str, version=spec_info.version, model_count=model_count
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
    return yaml.dump({"info": {"version": version}}) + yaml.dump(spec)

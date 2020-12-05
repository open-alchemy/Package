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
        raise exceptions.LoadSpecError("the schema is not valid") from exc
    final_spec_str = build.generate_spec(schemas=schemas)
    version = build.calculate_version(spec=spec, spec_str=spec_str)

    return TSpecInfo(spec_str=final_spec_str, version=version)

"""Helpers for spec."""

import json
import typing

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


def dump(*, spec: TSpec) -> str:
    """
    Serialize the spec.

    Args:
        spec: The spec to serialize.

    Returns:
        The serialized spec.

    """
    return json.dumps(spec)

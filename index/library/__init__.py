"""Library for the index application."""

import base64
import dataclasses

from . import exceptions


@dataclasses.dataclass
class Authorization:
    """Authorization information."""

    public_key: str
    secret_key: str


def parse_authorization_header(value: str) -> Authorization:
    """
    Parse the authorization header.

    Args:
        value: The value of the authorization header (in the form 'Basic <base 64
            encoded>').

    Returns:
        The public and secret key from the header.

    """
    expected_start = "Basic "
    if not value.startswith(expected_start):
        raise exceptions.UnauthorizedError(
            f'Authorization header does not start with "{expected_start}", {value=}'
        )

    encoded_token_str = value[len(expected_start) :]
    try:
        encoded_token_bytes = encoded_token_str.encode()
        decoded_token = base64.b64decode(encoded_token_bytes).decode()
    except ValueError as exc:
        raise exceptions.UnauthorizedError(
            f"could not decode token, {encoded_token_str=}, {value=}"
        ) from exc

    if decoded_token.count(":") != 1:
        raise exceptions.UnauthorizedError(
            f"decoded token has multiple values, {decoded_token=}, {value=}"
        )
    public_key, secret_key = decoded_token.split(":")
    if len(public_key) == 0:
        raise exceptions.UnauthorizedError(f"public key empty, {public_key=}, {value=}")
    if len(secret_key) == 0:
        raise exceptions.UnauthorizedError(f"secret key empty, {secret_key=}, {value=}")

    return Authorization(public_key=public_key, secret_key=secret_key)

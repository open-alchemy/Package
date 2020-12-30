"""Handle credentials requests."""

import json

from .. import types
from ..facades import server


def get(user: types.TUser) -> server.Response:
    """
    Retrieve the credentials for the user.

    Args:
        user: The user from the token.

    Returns:
        The credentials for the user.

    """
    print(user)  # allow-print
    return server.Response(
        json.dumps({"public_key": "pk_test", "secret_key": "sk_test"}),
        status=200,
        mimetype="application/json",
    )


def delete(user: types.TUser) -> server.Response:
    """
    Retrieve the credentials for the user.

    Args:
        user: The user from the token.

    Returns:
        The credentials for the user.

    """
    print(user)  # allow-print
    return server.Response(status=204)

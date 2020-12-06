"""Handle specs versions endpoint."""

from ... import types
from ...facades import server


def list_(spec_id: types.TSpecId, user: types.TUser) -> server.Response:
    """
    List all available versions of a spec.

    Args:
        spec_id: The id of the spec.
        user: The user from the token.

    Returns:
        The response to the request.

    """

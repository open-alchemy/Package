"""Handle specs versions endpoint."""

import json

from ... import types
from ...facades import server, storage


def list_(spec_id: types.TSpecId, user: types.TUser) -> server.Response:
    """
    List all available versions of a spec.

    Args:
        spec_id: The id of the spec.
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        return server.Response(
            json.dumps(
                storage.get_storage_facade().get_spec_versions(
                    user=user, spec_id=spec_id
                )
            ),
            status=200,
            mimetype="application/json",
        )
    except storage.exceptions.ObjectNotFoundError:
        return server.Response(
            f"could not find spec with id {spec_id}",
            status=404,
            mimetype="text/plain",
        )
    except storage.exceptions.StorageError:
        return server.Response(
            "something went wrong whilst reading from the storage",
            status=500,
            mimetype="text/plain",
        )

"""Handle specs versions endpoint."""

import json

from ... import types
from ...facades import server, storage
from ...helpers import spec


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


def get(
    spec_id: types.TSpecId, version: types.TSpecVersion, user: types.TUser
) -> server.Response:
    """
    Retrieve a version of a spec for a user.

    Args:
        spec_id: The id of the spec.
        version: The version of the spec to get
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        spec_str = storage.get_storage_facade().get_spec(
            user=user, spec_id=spec_id, version=version
        )
        prepared_spec_str = spec.prepare(spec_str=spec_str, version=version)

        return server.Response(
            prepared_spec_str,
            status=200,
            mimetype="text/plain",
        )
    except storage.exceptions.ObjectNotFoundError:
        return server.Response(
            f"could not find the spec with id {spec_id}",
            status=404,
            mimetype="text/plain",
        )
    except storage.exceptions.StorageError:
        return server.Response(
            "something went wrong whilst reading the spec",
            status=500,
            mimetype="text/plain",
        )

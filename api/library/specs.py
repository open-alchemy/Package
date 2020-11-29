"""Handle specs endpoint."""

from .facades import server, storage


def put(body: bytearray, spec_id: str, user: str) -> server.Response:
    """
    Accept a spec and store it.

    Args:
        body: The spec to store.
        spec_id: The id of the spec.
        user: The user from the token.

    """

    try:
        storage.get_storage().set(
            key=f"{user}/{spec_id}/spec.json", value=body.decode()
        )

        return server.Response(status=204)

    except storage.exceptions.StorageError:
        return server.Response(
            "something went wrong whilst storing the spec",
            status=500,
            mimetype="text/plain",
        )

"""Handle specs endpoint."""

from .facades import server, storage


def put(body: bytearray, spec_id: str) -> server.Response:
    """
    Accept a spec and store it.

    Args:
        body: The spec to store.
        spec_id: The id of the spec.

    """
    try:
        storage.get_storage().set(key=spec_id, value=body.decode())

        return server.Response(status=204)

    except storage.exceptions.StorageError:
        return server.Response(
            "something went wrong whilst storing the spec",
            status=500,
            mimetype="text/plain",
        )

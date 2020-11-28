"""Handle specs endpoint."""

from .facades import server, storage


def put(body: str, spec_id: str) -> server.Response:
    """
    Accept a spec and store it.

    Args:
        body: The spec to store.
        spec_id: The id of the spec.

    """
    storage.get_storage().set(key=spec_id, value=body)

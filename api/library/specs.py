"""Handle specs endpoint."""

import json

from .facades import server, storage, database
from .helpers import spec
from . import exceptions


def list_(user: str) -> server.Response:
    """
    Accept a spec and store it.

    Args:
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        return server.Response(
            json.dumps(database.get_database().list_specs(sub=user)),
            status=200,
            mimetype="application/json",
        )
    except database.exceptions.DatabaseError:
        return server.Response(
            "something went wrong whilst reading from the database",
            status=500,
            mimetype="text/plain",
        )


def get(spec_id: str, user: str) -> server.Response:
    """
    Retrieve a spec for a user.

    Args:
        spec_id: The id of the spec.
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        version = database.get_database().get_latest_spec_version(
            sub=user, spec_id=spec_id
        )
        spec_str = storage.get_storage().get(
            key=f"{user}/{spec_id}/{version}-spec.json"
        )
        prepared_spec_str = spec.prepare(spec_str=spec_str, version=version)

        return server.Response(
            prepared_spec_str,
            status=200,
            mimetype="text/plain",
        )
    except database.exceptions.NotFoundError:
        return server.Response(
            f"could not find the spec with id {spec_id}",
            status=404,
            mimetype="text/plain",
        )
    except database.exceptions.DatabaseError:
        return server.Response(
            "something went wrong whilst reading from the database",
            status=500,
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


def put(body: bytearray, spec_id: str, user: str) -> server.Response:
    """
    Accept a spec and store it.

    Args:
        body: The spec to store.
        spec_id: The id of the spec.
        user: The user from the token.

    Returns:
        The response to the request.

    """
    language = server.Request.request.headers["X-LANGUAGE"]

    try:
        # Check whether spec is valid
        spec_info = spec.process(spec_str=body.decode(), language=language)

        # Check that the maximum number of models hasn't been exceeded
        current_count = database.get_database().count_customer_models(sub=user)
        if current_count + spec_info.model_count > 100:
            return server.Response(
                "with this spec the maximum number of 100 models for the free trial "
                f"would be exceeded, current models count: {current_count}, "
                f"models in this spec: {spec_info.model_count}",
                status=402,
                mimetype="text/plain",
            )

        # Store the spec
        storage.get_storage().set(
            key=f"{user}/{spec_id}/{spec_info.version}-spec.json",
            value=spec_info.spec_str,
        )

        # Write an update into the database
        database.get_database().create_update_spec(
            sub=user,
            spec_id=spec_id,
            version=spec_info.version,
            model_count=spec_info.model_count,
        )

        return server.Response(status=204)

    except exceptions.LoadSpecError as exc:
        return server.Response(
            f"the spec is not valid, {exc}",
            status=400,
            mimetype="text/plain",
        )
    except storage.exceptions.StorageError:
        return server.Response(
            "something went wrong whilst storing the spec",
            status=500,
            mimetype="text/plain",
        )
    except database.exceptions.DatabaseError:
        return server.Response(
            "something went wrong whilst updating the database",
            status=500,
            mimetype="text/plain",
        )

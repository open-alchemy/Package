"""Handle specs endpoint."""

import json

from open_alchemy import package_database

from .. import exceptions, types
from ..facades import server, storage
from ..helpers import spec


def list_(user: types.TUser) -> server.Response:
    """
    Accept a spec and store it.

    Args:
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        return server.Response(
            json.dumps(
                list(map(spec.add_spec_id, package_database.get().list_specs(sub=user)))
            ),
            status=200,
            mimetype="application/json",
        )
    except package_database.exceptions.BaseError:
        return server.Response(
            "something went wrong whilst reading from the database",
            status=500,
            mimetype="text/plain",
        )


def get(spec_id: types.TSpecId, user: types.TUser) -> server.Response:
    """
    Retrieve a spec for a user.

    Args:
        spec_id: The id of the spec.
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        version = package_database.get().get_latest_spec_version(sub=user, id_=spec_id)
        spec_str = storage.get_storage_facade().get_spec(
            user=user, spec_id=spec_id, version=version
        )
        prepared_spec_str = spec.prepare(spec_str=spec_str, version=version)

        return server.Response(
            prepared_spec_str,
            status=200,
            mimetype="text/plain",
        )
    except package_database.exceptions.NotFoundError:
        return server.Response(
            f"could not find the spec with id {spec_id}",
            status=404,
            mimetype="text/plain",
        )
    except package_database.exceptions.BaseError:
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


def put(body: bytearray, spec_id: types.TSpecId, user: types.TUser) -> server.Response:
    """
    Accept a spec and store it.

    Returns 400 if the spec is not valid.
    Returns 402 if the free tier is exceeded.
    Returns 500 if something went wrong.

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
        free_tier_check = package_database.get().check_would_exceed_free_tier(
            sub=user, model_count=spec_info.model_count
        )
        if free_tier_check.result:
            return server.Response(
                free_tier_check.reason,
                status=402,
                mimetype="text/plain",
            )

        # Store the spec
        storage.get_storage_facade().create_update_spec(
            user=user,
            spec_id=spec_id,
            version=spec_info.version,
            spec_str=spec_info.spec_str,
        )

        # Write an update into the database
        package_database.get().create_update_spec(
            sub=user,
            id_=spec_id,
            version=spec_info.version,
            title=spec_info.title,
            description=spec_info.description,
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
    except package_database.exceptions.BaseError:
        return server.Response(
            "something went wrong whilst updating the database",
            status=500,
            mimetype="text/plain",
        )


def delete(spec_id: types.TSpecId, user: types.TUser) -> server.Response:
    """
    Delete a spec for a user.

    Args:
        spec_id: The id of the spec.
        user: The user from the token.

    Returns:
        The response to the request.

    """
    try:
        package_database.get().delete_spec(sub=user, id_=spec_id)
    except package_database.exceptions.BaseError:
        pass
    try:
        storage.get_storage_facade().delete_spec(user=user, spec_id=spec_id)
    except storage.exceptions.StorageError:
        pass

    return server.Response(status=204)

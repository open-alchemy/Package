"""Handle credentials requests."""

import json

from open_alchemy import package_database, package_security

from .. import config, types
from ..facades import server


def get(user: types.TUser) -> server.Response:
    """
    Retrieve the credentials for the user.

    Args:
        user: The user from the token.

    Returns:
        The credentials for the user.

    """
    public_key: str
    secret_key: str
    id_ = config.get().default_credentials_id

    # Retrieve or create credentials
    stored_credentials = package_database.get().get_credentials(sub=user, id_=id_)
    if stored_credentials is not None:
        public_key = stored_credentials["public_key"]
        secret_key = package_security.retrieve_secret_key(
            sub=user, salt=stored_credentials["salt"]
        )
    else:
        created_credentials = package_security.create(sub=user)
        public_key = created_credentials.public_key
        secret_key = created_credentials.secret_key
        package_database.get().create_update_credentials(
            sub=user,
            id_=id_,
            public_key=public_key,
            secret_key_hash=created_credentials.secret_key_hash,
            salt=created_credentials.salt,
        )

    return server.Response(
        json.dumps(
            {
                "public_key": public_key,
                "secret_key": secret_key,
            }
        ),
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
    package_database.get().delete_credentials(
        sub=user, id_=config.get().default_credentials_id
    )
    return server.Response(status=204)

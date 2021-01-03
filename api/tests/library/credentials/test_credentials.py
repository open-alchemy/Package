"""Tests for credentials."""

import json

import pytest
from library import config, credentials
from open_alchemy import package_database, package_security


@pytest.mark.credentials
def test_get_credentials_not_exist():
    """
    GIVEN empty database
    WHEN get is called
    THEN credentials are created in the database and returned.
    """
    user = "user 1"

    response = credentials.get(user)

    stored_credentials = package_database.get().get_credentials(sub=user, id_="default")
    assert stored_credentials is not None

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    returned_credentials = json.loads(response.data.decode())

    assert "public_key" in returned_credentials
    assert returned_credentials["public_key"] == stored_credentials["public_key"]
    assert "secret_key" in returned_credentials


@pytest.mark.credentials
def test_get_credentials_exist():
    """
    GIVEN database with credentials
    WHEN get is called
    THEN the credentials are returned.
    """
    user = "user 1"
    created_credentials = package_security.create(sub=user)
    package_database.get().create_update_credentials(
        sub=user,
        id_="default",
        public_key=created_credentials.public_key,
        secret_key_hash=created_credentials.secret_key_hash,
        salt=created_credentials.salt,
    )

    response = credentials.get(user)

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    returned_credentials = json.loads(response.data.decode())

    assert "public_key" in returned_credentials
    assert returned_credentials["public_key"] == created_credentials.public_key
    assert "secret_key" in returned_credentials
    assert returned_credentials["secret_key"] == created_credentials.secret_key


@pytest.mark.credentials
def test_delete_credentials_not_exist():
    """
    GIVEN empty database
    WHEN delete is called
    THEN.
    """
    user = "user 1"

    response = credentials.delete(user)

    assert response.status_code == 204


@pytest.mark.credentials
def test_delete_credentials_exist():
    """
    GIVEN database with credentials
    WHEN delete is called
    THEN the credentials are deleted.
    """
    user = "user 1"
    created_credentials = package_security.create(sub=user)
    package_database.get().create_update_credentials(
        sub=user,
        id_=config.get().default_credentials_id,
        public_key=created_credentials.public_key,
        secret_key_hash=created_credentials.secret_key_hash,
        salt=created_credentials.salt,
    )

    response = credentials.delete(user)

    assert response.status_code == 204
    assert (
        package_database.get().get_credentials(
            sub=user, id_=config.get().default_credentials_id
        )
        is None
    )

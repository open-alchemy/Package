"""Database production tests."""

import pytest
from open_alchemy import package_database


def test_spec_create_list_delete_all(sub):
    """
    GIVEN spec values
    WHEN spec is created, listed and all are deleted
    THEN the spec is returned in the list after creation but not after deletion.
    """
    name = "NAME 1"
    model_count = 1
    version = "version 1"
    title = "title 1"
    description = "description 1"

    database_instance = package_database.get()

    assert len(database_instance.list_specs(sub=sub)) == 0

    database_instance.create_update_spec(
        sub=sub,
        name=name,
        model_count=model_count,
        version=version,
        title=title,
        description=description,
    )

    infos = database_instance.list_specs(sub=sub)
    assert len(infos) == 1
    info = infos[0]
    assert info["name"] == name
    assert info["id"] == name.lower()
    assert info["model_count"] == model_count
    assert info["version"] == version
    assert info["title"] == title
    assert info["description"] == description

    database_instance.delete_all_specs(sub=sub)

    assert len(database_instance.list_specs(sub=sub)) == 0


def test_spec_create_count_models_get_latest_version_list_versions_delete(sub):
    """
    GIVEN spec values
    WHEN the models are counted, the latest version is retrieved, versions are listed
        and deleted
    THEN the model count for the spec is returned, the version of the spec is returned,
        the version of the spec is listed after creation but not after deletion.
    """
    name = "name 1"
    model_count = 1
    version = "version 1"

    database_instance = package_database.get()

    assert len(database_instance.list_specs(sub=sub)) == 0

    database_instance.create_update_spec(
        sub=sub, name=name, model_count=model_count, version=version
    )

    assert database_instance.count_customer_models(sub=sub) == model_count

    info = database_instance.get_spec(sub=sub, name=name)

    assert info["name"] == name
    assert info["id"] == name
    assert info["version"] == version
    assert info["model_count"] == model_count

    assert database_instance.get_latest_spec_version(sub=sub, name=name) == version

    infos = database_instance.list_spec_versions(sub=sub, name=name)
    assert len(infos) == 1
    info = infos[0]
    assert info["name"] == name
    assert info["id"] == name
    assert info["model_count"] == model_count
    assert info["version"] == version

    database_instance.delete_spec(sub=sub, name=name)

    assert database_instance.count_customer_models(sub=sub) == 0

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.get_latest_spec_version(sub=sub, name=name)

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.list_spec_versions(sub=sub, name=name)


def test_credentials_create_list_delete_all(sub):
    """
    GIVEN credentials values
    WHEN credentials are created, listed and all are deleted
    THEN the credentials are returned in the list after creation but not after deletion.
    """
    id_ = "id 1"
    public_key = "public key 1"
    secret_key_hash = b"secret key has 1"
    salt = b"salt 1"

    database_instance = package_database.get()

    assert len(database_instance.list_credentials(sub=sub)) == 0

    database_instance.create_update_credentials(
        sub=sub,
        id_=id_,
        public_key=public_key,
        secret_key_hash=secret_key_hash,
        salt=salt,
    )

    infos = database_instance.list_credentials(sub=sub)
    assert len(infos) == 1
    info = infos[0]
    assert info["id"] == id_
    assert info["public_key"] == public_key
    assert info["salt"] == salt

    database_instance.delete_all_credentials(sub=sub)

    assert len(database_instance.list_credentials(sub=sub)) == 0


def test_credentials_create_get_get_user_delete(sub):
    """
    GIVEN credentials values
    WHEN credentials are created, retrieved, the user is retrieved and deleted
    THEN the credentials and user are returned after creation but not after deletion.
    """
    id_ = "id 1"
    public_key = "public key 1"
    secret_key_hash = b"secret key has 1"
    salt = b"salt 1"

    database_instance = package_database.get()

    assert len(database_instance.list_credentials(sub=sub)) == 0

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.get_credentials(sub=sub, id_=id_)

    auth_info = database_instance.get_user(public_key=public_key)

    assert auth_info is None

    database_instance.create_update_credentials(
        sub=sub,
        id_=id_,
        public_key=public_key,
        secret_key_hash=secret_key_hash,
        salt=salt,
    )

    info = database_instance.get_credentials(sub=sub, id_=id_)
    assert info["id"] == id_
    assert info["public_key"] == public_key
    assert info["salt"] == salt

    auth_info = database_instance.get_user(public_key=public_key)
    assert auth_info.sub == sub
    assert auth_info.secret_key_hash == secret_key_hash
    assert auth_info.salt == salt

    database_instance.delete_credentials(sub=sub, id_=id_)

    info = database_instance.get_credentials(sub=sub, id_=id_)

    assert info is None

    auth_info = database_instance.get_user(public_key=public_key)

    assert auth_info is None

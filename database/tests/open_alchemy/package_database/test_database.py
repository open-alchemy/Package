"""Tests for database facade."""

import time
from unittest import mock

import pytest
from open_alchemy import package_database


def test_count_customer_models(_clean_specs_table):
    """
    GIVEN sub, name, version and model count
    WHEN create_update_spec is called with the spec info and count_customer_models is
        called
    THEN the model count is returned.
    """
    sub = "sub 1"
    database_instance = package_database.get()

    assert database_instance.count_customer_models(sub=sub) == 0

    name = "name 1"
    version = "version 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub, name=name, version=version, model_count=model_count_1
    )

    assert database_instance.count_customer_models(sub=sub) == model_count_1

    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, name=name, version=version, model_count=model_count_2
    )

    assert database_instance.count_customer_models(sub=sub) == model_count_2

    assert database_instance.count_customer_models(sub="sub 2") == 0


@pytest.mark.parametrize(
    "initial_count, additional_count, expected_result",
    [
        pytest.param(0, 0, False, id="zero initial count, zero additional"),
        pytest.param(
            0, 9, False, id="zero initial count, just less than limit additional"
        ),
        pytest.param(0, 10, False, id="zero initial count, equal to limit additional"),
        pytest.param(
            0, 11, True, id="zero initial count, just more than limit additional"
        ),
        pytest.param(0, 15, True, id="zero initial count, more than limit additional"),
        pytest.param(
            9, 0, False, id="just less than limit initial count, zero additional"
        ),
        pytest.param(10, 0, False, id="equal to limit initial count, zero additional"),
        pytest.param(
            11, 0, True, id="just more than limit initial count, zero additional"
        ),
        pytest.param(15, 0, True, id="more than limit initial count, zero additional"),
        pytest.param(
            5, 4, False, id="sum of initial and additional just less than limit"
        ),
        pytest.param(5, 5, False, id="sum of initial and additional equal to limit"),
        pytest.param(
            5, 6, True, id="sum of initial and additional just more than limit"
        ),
    ],
)
def test_check_would_exceed_free_tier(
    initial_count, additional_count, expected_result, _clean_specs_table
):
    """
    GIVEN initial count and additional count
    WHEN create_update_spec is called with the initial count and
        check_would_exceed_free_tier with the additional count
    THEN the expected result is returned
    """
    sub = "sub 1"
    name = "name 1"
    version = "version 1"
    database_instance = package_database.get()

    database_instance.create_update_spec(
        sub=sub, name=name, version=version, model_count=initial_count
    )

    returned_result = database_instance.check_would_exceed_free_tier(
        sub=sub, model_count=additional_count
    )

    assert returned_result.result == expected_result


def test_get_latest_spec_version(_clean_specs_table):
    """
    GIVEN sub, name, version and model count
    WHEN create_update_spec is called with the spec info and get_latest_spec_version is
        called
    THEN the latest version is returned.
    """
    sub = "sub 1"
    name = "name 1"
    database_instance = package_database.get()

    with pytest.raises(package_database.exceptions.BaseError):
        database_instance.get_latest_spec_version(sub=sub, name=name)

    version_1 = "version 1"
    model_count = 1
    database_instance.create_update_spec(
        sub=sub, name=name, version=version_1, model_count=model_count
    )

    assert database_instance.get_latest_spec_version(sub=sub, name=name) == version_1

    version_2 = "version 2"
    database_instance.create_update_spec(
        sub=sub, name=name, version=version_2, model_count=model_count
    )

    assert database_instance.get_latest_spec_version(sub=sub, name=name) == version_2

    with pytest.raises(package_database.exceptions.BaseError):
        database_instance.get_latest_spec_version(sub=sub, name="name 2")

    with pytest.raises(package_database.exceptions.BaseError):
        database_instance.get_latest_spec_version(sub="sub 2", name=name)


def test_list_delete_all_spec(_clean_specs_table):
    """
    GIVEN sub, name, version and model count
    WHEN create_update_spec is called with the spec info and list_specs is called
    THEN all specs for the customer are returned.
    """
    sub = "sub 1"
    database_instance = package_database.get()

    assert database_instance.list_specs(sub=sub) == []

    name_1 = "name 1"
    version_1 = "version 1"
    title = "title 1"
    description = "description 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub,
        name=name_1,
        version=version_1,
        model_count=model_count_1,
        title=title,
        description=description,
    )

    spec_infos = database_instance.list_specs(sub=sub)
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["name"] == name_1
    assert spec_info["id"] == name_1
    assert spec_info["version"] == version_1
    assert spec_info["title"] == title
    assert spec_info["description"] == description
    assert spec_info["model_count"] == model_count_1
    assert "updated_at" in spec_info

    name_2 = "name 2"
    version_2 = "version 2"
    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, name=name_2, version=version_2, model_count=model_count_2
    )

    spec_infos = database_instance.list_specs(sub=sub)
    assert len(spec_infos) == 2
    assert spec_infos[0]["name"] == name_1
    assert spec_infos[0]["id"] == name_1
    spec_info = spec_infos[1]
    assert spec_info["name"] == name_2
    assert spec_info["id"] == name_2
    assert spec_info["version"] == version_2
    assert spec_info["model_count"] == model_count_2
    assert "updated_at" in spec_info

    database_instance.delete_all_specs(sub=sub)

    assert database_instance.list_specs(sub=sub) == []


def test_get_spec(_clean_specs_table):
    """
    GIVEN sub, name, version and model count
    WHEN create_update_spec is called with the spec info and get_spec is called
    THEN the spec info is returned.
    """
    sub = "sub 1"
    name = "name 1"
    database_instance = package_database.get()

    returned_info = database_instance.get_spec(sub=sub, name=name)

    assert returned_info is None

    version = "version 1"
    model_count = 1
    database_instance.create_update_spec(
        sub=sub, name=name, version=version, model_count=model_count
    )

    returned_info = database_instance.get_spec(sub=sub, name=name)

    assert returned_info["name"] == name
    assert returned_info["id"] == name
    assert returned_info["version"] == version
    assert returned_info["model_count"] == model_count


def test_delete_spec(_clean_specs_table):
    """
    GIVEN sub, name, version and model count
    WHEN create_update_spec is called with the spec info and delete_spec is called
    THEN the spec is deleted.
    """
    sub = "sub 1"
    name = "name 1"
    version = "version 1"
    model_count = 1
    database_instance = package_database.get()
    database_instance.create_update_spec(
        sub=sub, name=name, version=version, model_count=model_count
    )

    assert len(database_instance.list_specs(sub=sub)) == 1
    assert database_instance.count_customer_models(sub=sub) == model_count
    assert database_instance.get_latest_spec_version(sub=sub, name=name) == version

    database_instance.delete_spec(sub=sub, name=name)

    assert len(database_instance.list_specs(sub=sub)) == 0
    assert database_instance.count_customer_models(sub=sub) == 0
    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.get_latest_spec_version(sub=sub, name=name)


def test_list_spec_versions(monkeypatch, _clean_specs_table):
    """
    GIVEN sub, name, version and model count
    WHEN create_update_spec is called with the spec info and list_spec_versions is
        called
    THEN all specs for the customer are returned or NotFoundError is raised.
    """
    mock_time = mock.MagicMock()
    monkeypatch.setattr(time, "time", mock_time)
    sub = "sub 1"
    name = "name 1"
    database_instance = package_database.get()

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.list_spec_versions(sub=sub, name=name)

    mock_time.return_value = 1000000
    version_1 = "version 1"
    title = "title 1"
    description = "description 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub,
        name=name,
        version=version_1,
        model_count=model_count_1,
        title=title,
        description=description,
    )

    spec_infos = database_instance.list_spec_versions(sub=sub, name=name)
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["name"] == name
    assert spec_info["id"] == name
    assert spec_info["version"] == version_1
    assert spec_info["title"] == title
    assert spec_info["description"] == description
    assert spec_info["model_count"] == model_count_1
    assert "updated_at" in spec_info

    mock_time.return_value = 2000000
    version_2 = "version 2"
    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, name=name, version=version_2, model_count=model_count_2
    )

    spec_infos = database_instance.list_spec_versions(sub=sub, name=name)
    assert len(spec_infos) == 2
    assert spec_infos[0]["name"] == name
    assert spec_infos[0]["id"] == name
    spec_info = spec_infos[1]
    assert spec_info["name"] == name
    assert spec_info["id"] == name
    assert spec_info["version"] == version_2
    assert spec_info["model_count"] == model_count_2
    assert "updated_at" in spec_info


def test_create_list_delete_all_credentials(_clean_credentials_table):
    """
    GIVE multiple credentials
    WHEN credentials are created, listed and deleted
    THEN all created credentials are listed and subsequently deleted.
    """
    sub_1 = "sub 1"

    database_instance = package_database.get()
    assert len(database_instance.list_credentials(sub=sub_1)) == 0

    database_instance.create_update_credentials(
        sub=sub_1,
        id_="id 1",
        public_key="public key 1",
        secret_key_hash=b"secret key hash 1",
        salt=b"salt 1",
    )

    assert len(database_instance.list_credentials(sub=sub_1)) == 1

    sub_2 = "sub 2"

    assert len(database_instance.list_credentials(sub=sub_2)) == 0

    database_instance.create_update_credentials(
        sub=sub_2,
        id_="id 2",
        public_key="public key 2",
        secret_key_hash=b"secret key hash 2",
        salt=b"salt 2",
    )

    assert len(database_instance.list_credentials(sub=sub_2)) == 1

    database_instance.delete_all_credentials(sub=sub_1)

    assert len(database_instance.list_credentials(sub=sub_1)) == 0
    assert len(database_instance.list_credentials(sub=sub_2)) == 1


def test_create_get_get_user_delete_credentials(_clean_credentials_table):
    """
    GIVE single credentials
    WHEN credentials are created, retrieved, user is retrieved and deleted
    THEN all the created credentials and user are returned and then deleted.
    """
    sub = "sub 1"
    id_ = "id 1"
    public_key_1 = "public key 1"
    secret_key_hash_1 = b"secret key hash 1"
    salt_1 = b"salt 1"

    database_instance = package_database.get()
    info = database_instance.get_credentials(sub=sub, id_=id_)

    assert info is None

    auth_info = database_instance.get_user(public_key=public_key_1)

    assert auth_info is None

    database_instance.create_update_credentials(
        sub=sub,
        id_=id_,
        public_key=public_key_1,
        secret_key_hash=secret_key_hash_1,
        salt=salt_1,
    )

    info = database_instance.get_credentials(sub=sub, id_=id_)

    assert info["id"] == id_
    assert info["public_key"] == public_key_1
    assert info["salt"] == salt_1

    auth_info = database_instance.get_user(public_key=public_key_1)

    assert auth_info.sub == sub
    assert auth_info.secret_key_hash == secret_key_hash_1
    assert auth_info.salt == salt_1

    public_key_2 = "public key 2"
    secret_key_hash_2 = b"secret key hash 2"
    salt_2 = b"salt 2"

    database_instance.create_update_credentials(
        sub=sub,
        id_=id_,
        public_key=public_key_2,
        secret_key_hash=secret_key_hash_2,
        salt=salt_2,
    )

    info = database_instance.get_credentials(sub=sub, id_=id_)

    assert info["public_key"] == public_key_2
    assert info["salt"] == salt_2

    auth_info = database_instance.get_user(public_key=public_key_2)

    assert auth_info.secret_key_hash == secret_key_hash_2
    assert auth_info.salt == salt_2

    database_instance.delete_credentials(sub=sub, id_=id_)

    info = database_instance.get_credentials(sub=sub, id_=id_)

    assert info is None

    auth_info = database_instance.get_user(public_key=public_key_1)

    assert auth_info is None


def test_delete_all(_clean_specs_table, _clean_credentials_table):
    """
    GIVEN database with spec and credentials
    WHEN delete_all is called
    THEN all spec and credentials are deleted.
    """
    sub = "sub 1"

    database_instance = package_database.get()
    database_instance.create_update_credentials(
        sub=sub,
        id_="id 1",
        public_key="public key 1",
        secret_key_hash=b"secret key hash 1",
        salt=b"salt 1",
    )
    database_instance.create_update_spec(
        sub=sub, name="name 1", version="version 1", model_count=1
    )

    assert len(database_instance.list_specs(sub=sub)) == 1
    assert len(database_instance.list_credentials(sub=sub)) == 1

    database_instance.delete_all(sub=sub)

    assert len(database_instance.list_specs(sub=sub)) == 0
    assert len(database_instance.list_credentials(sub=sub)) == 0

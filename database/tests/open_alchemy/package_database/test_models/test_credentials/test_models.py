"""Tests for the models."""

import pytest
from open_alchemy.package_database import factory, models

LIST_CREDENTIALS_TESTS = [
    pytest.param([], "sub 1", [], id="empty"),
    pytest.param(
        [factory.CredentialsFactory(sub="sub 1")],
        "sub 2",
        [],
        id="single sub miss",
    ),
    pytest.param(
        [factory.CredentialsFactory(sub="sub 1")],
        "sub 1",
        [0],
        id="single hit",
    ),
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1"),
            factory.CredentialsFactory(sub="sub 2"),
        ],
        "sub 3",
        [],
        id="multiple miss",
    ),
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1"),
            factory.CredentialsFactory(sub="sub 2"),
        ],
        "sub 1",
        [0],
        id="multiple first hit",
    ),
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1"),
            factory.CredentialsFactory(sub="sub 2"),
        ],
        "sub 2",
        [1],
        id="multiple second hit",
    ),
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1"),
            factory.CredentialsFactory(sub="sub 1"),
        ],
        "sub 1",
        [0, 1],
        id="multiple hit",
    ),
]


@pytest.mark.parametrize("items, sub, expected_idx_list", LIST_CREDENTIALS_TESTS)
def test_list_credentials(items, sub, expected_idx_list):
    """
    GIVEN items in the database and sub
    WHEN list_credentials is called on Spec with the sub
    THEN the expected ids are returned.
    """
    for item in items:
        item.save()

    returned_infos = models.Credentials.list_credentials(sub=sub)

    expected_infos = list(
        map(
            models.Credentials.item_to_info,
            map(lambda idx: items[idx], expected_idx_list),
        )
    )
    assert returned_infos == expected_infos


def test_create_update_item():
    """
    GIVEN credentials properties and empty database
    WHEN create_update_item is called with the credentials properties and then updated
    THEN the credentials are written to the database and can be queried using indexes.
    """
    sub = "sub 1"
    id_ = "id 1"
    public_key_1 = "public key 1"
    secret_key_hash_1 = b"secret key hash 1"
    salt_1 = b"salt 1"

    models.Credentials.create_update_item(
        sub=sub,
        id_=id_,
        public_key=public_key_1,
        secret_key_hash=secret_key_hash_1,
        salt=salt_1,
    )

    created_item = models.Credentials.get(hash_key=sub, range_key=id_)
    assert created_item.public_key == public_key_1
    assert created_item.secret_key_hash == secret_key_hash_1
    assert created_item.salt == salt_1

    assert len(list(models.Credentials.scan())) == 1
    assert (
        len(list(models.Credentials.public_key_index.query(hash_key=public_key_1))) == 1
    )

    public_key_2 = "public key 2"
    secret_key_hash_2 = b"secret key hash 2"
    salt_2 = b"salt 2"

    models.Credentials.create_update_item(
        sub=sub,
        id_=id_,
        public_key=public_key_2,
        secret_key_hash=secret_key_hash_2,
        salt=salt_2,
    )

    updated_item = models.Credentials.get(hash_key=sub, range_key=id_)
    assert updated_item.public_key == public_key_2
    assert updated_item.secret_key_hash == secret_key_hash_2
    assert updated_item.salt == salt_2

    assert len(list(models.Credentials.scan())) == 1
    assert (
        len(list(models.Credentials.public_key_index.query(hash_key=public_key_1))) == 0
    )
    assert (
        len(list(models.Credentials.public_key_index.query(hash_key=public_key_2))) == 1
    )


PARTITION_SORT_KEY_TESTS = [
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1", id="id 1"),
            factory.CredentialsFactory(sub="sub 1", id="id 1"),
        ],
        1,
        id="same partition sort",
    ),
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1", id="id 1"),
            factory.CredentialsFactory(sub="sub 2", id="id 1"),
        ],
        2,
        id="same partition different",
    ),
    pytest.param(
        [
            factory.CredentialsFactory(sub="sub 1", id="id 1"),
            factory.CredentialsFactory(sub="sub 1", id="id 2"),
        ],
        2,
        id="same sort different",
    ),
]


@pytest.mark.parametrize("items, expected_item_count", PARTITION_SORT_KEY_TESTS)
def test_partition_sort_key(items, expected_item_count):
    """
    GIVEN items
    WHEN they are saved
    THEN the expected number of items are in the database.
    """
    for item in items:
        item.save()

    assert len(list(models.Credentials.scan())) == expected_item_count


def test_item_to_info():
    """
    GIVEN properties for credentials
    WHEN Credentials are constructed and item_to_info is called
    THEN the expected info is returned.
    """
    item = factory.CredentialsFactory()

    spec_info = models.Credentials.item_to_info(item)

    assert spec_info["id"] == item.id
    assert spec_info["public_key"] == item.public_key
    assert spec_info["salt"] == item.salt

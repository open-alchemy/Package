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

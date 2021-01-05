"""Tests for the models."""

import pytest
from open_alchemy.package_database import factory, models

DELETE_ITEM_TESTS = [
    pytest.param([], "sub 1", "name 1", 0, id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            )
        ],
        "sub 2",
        "name 1",
        1,
        id="single sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            )
        ],
        "sub 1",
        "name 2",
        1,
        id="single id miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            )
        ],
        "sub 1",
        "name 1",
        0,
        id="single hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="NAME 1",
                id="name 1",
                id_updated_at="name 1#11",
            )
        ],
        "sub 1",
        "NAME 1",
        0,
        id="single hit different canonical name",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            ),
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#21",
            ),
        ],
        "sub 1",
        "name 1",
        0,
        id="multiple hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            ),
            factory.SpecFactory(
                sub="sub 2",
                name="name 2",
                id="name 2",
                id_updated_at="name 2#21",
            ),
        ],
        "sub 1",
        "name 1",
        1,
        id="multiple first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            ),
            factory.SpecFactory(
                sub="sub 2",
                name="name 2",
                id="name 2",
                id_updated_at="name 2#21",
            ),
        ],
        "sub 2",
        "name 2",
        1,
        id="multiple second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                id_updated_at="name 1#11",
            ),
            factory.SpecFactory(
                sub="sub 2",
                name="name 2",
                id="name 2",
                id_updated_at="name 2#21",
            ),
        ],
        "sub 3",
        "name 3",
        2,
        id="multiple miss",
    ),
]


@pytest.mark.parametrize("items, sub, name, expected_item_count", DELETE_ITEM_TESTS)
@pytest.mark.models
def test_delete_item(items, sub, name, expected_item_count):
    """
    GIVEN items in the database and sub and spec name
    WHEN delete_item is called on Spec with the sub and spec name
    THEN the expected number of items in the database remain.
    """
    for item in items:
        item.save()

    models.Spec.delete_item(sub=sub, name=name)

    assert len(list(models.Spec.scan())) == expected_item_count

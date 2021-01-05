"""Tests for the models."""

import pytest
from open_alchemy.package_database import factory, models

DELETE_ALL_TESTS = [
    pytest.param([], "sub 1", 0, id="empty"),
    pytest.param([factory.SpecFactory(sub="sub 1")], "sub 2", 1, id="single sub miss"),
    pytest.param([factory.SpecFactory(sub="sub 1")], "sub 1", 0, id="single sub hit"),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1"),
            factory.SpecFactory(sub="sub 2"),
        ],
        "sub 3",
        2,
        id="multiple sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1"),
            factory.SpecFactory(sub="sub 2"),
        ],
        "sub 1",
        1,
        id="multiple sub first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1"),
            factory.SpecFactory(sub="sub 2"),
        ],
        "sub 2",
        1,
        id="multiple sub second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1"),
            factory.SpecFactory(sub="sub 1"),
        ],
        "sub 1",
        0,
        id="multiple sub hit",
    ),
]


@pytest.mark.parametrize("items, sub, expected_count", DELETE_ALL_TESTS)
@pytest.mark.models
def test_delete_all(items, sub, expected_count):
    """
    GIVEN database with items and sub
    WHEN delete_all is called with the sub
    THEN the database contains the expected number of items.
    """
    for item in items:
        item.save()
    assert len(list(models.Spec.scan())) == len(items)

    models.Spec.delete_all(sub=sub)

    assert len(list(models.Spec.scan())) == expected_count

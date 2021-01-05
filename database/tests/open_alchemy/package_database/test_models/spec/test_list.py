"""Tests for the models."""

import pytest
from open_alchemy.package_database import factory, models

LIST_SPECS_TESTS = [
    pytest.param([], "sub 1", [], id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            )
        ],
        "sub 2",
        [],
        id="single sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id="11#",
            )
        ],
        "sub 1",
        [],
        id="single updated_at_id miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            )
        ],
        "sub 1",
        [0],
        id="single hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1", updated_at_id="11#"),
            factory.SpecFactory(sub="sub 2", updated_at_id="21#"),
        ],
        "sub 3",
        [],
        id="multiple miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            ),
            factory.SpecFactory(sub="sub 2", updated_at_id="21#"),
        ],
        "sub 1",
        [0],
        id="multiple first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1", updated_at_id="11#"),
            factory.SpecFactory(
                sub="sub 2",
                name="name 2",
                id="name 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 2"),
            ),
        ],
        "sub 2",
        [1],
        id="multiple second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            ),
            factory.SpecFactory(
                sub="sub 1",
                name="name 2",
                id="name 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 2"),
            ),
        ],
        "sub 1",
        [0, 1],
        id="multiple hit",
    ),
]


@pytest.mark.parametrize("items, sub, expected_idx_list", LIST_SPECS_TESTS)
@pytest.mark.models
def test_list_(items, sub, expected_idx_list):
    """
    GIVEN items in the database and sub
    WHEN list_ is called on Spec with the sub
    THEN the expected spec ids are returned.
    """
    for item in items:
        item.save()

    returned_spec_infos = models.Spec.list_(sub=sub)

    expected_spec_info = list(
        map(
            models.Spec.item_to_info,
            map(lambda idx: items[idx], expected_idx_list),
        )
    )
    assert returned_spec_infos == expected_spec_info

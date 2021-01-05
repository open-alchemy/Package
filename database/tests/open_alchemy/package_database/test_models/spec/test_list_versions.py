"""Tests for the models."""

import pytest
from open_alchemy.package_database import factory, models

LIST_VERSIONS_TESTS = [
    pytest.param([], "sub 1", "name 1", [], id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            )
        ],
        "sub 2",
        "name 1",
        [],
        id="single sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            )
        ],
        "sub 1",
        "name 2",
        [],
        id="single name miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at=(f"name 1#{models.Spec.UPDATED_AT_LATEST}"),
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            )
        ],
        "sub 1",
        "name 1",
        [],
        id="single updated at miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            )
        ],
        "sub 1",
        "name 1",
        [0],
        id="single hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            )
        ],
        "sub 1",
        "NAME 1",
        [0],
        id="single different canonical name",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            ),
            factory.SpecFactory(
                sub="sub 2",
                updated_at="21",
                id_updated_at="name 2#21",
                updated_at_id="21#name 2",
            ),
        ],
        "sub 3",
        "name 3",
        [],
        id="multiple miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            ),
            factory.SpecFactory(
                sub="sub 2",
                updated_at="21",
                id_updated_at="name 2#21",
                updated_at_id="21#name 2",
            ),
        ],
        "sub 1",
        "name 1",
        [0],
        id="multiple first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            ),
            factory.SpecFactory(
                sub="sub 2",
                updated_at="21",
                id_updated_at="name 2#21",
                updated_at_id="21#name 2",
            ),
        ],
        "sub 2",
        "name 2",
        [1],
        id="multiple second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            ),
            factory.SpecFactory(
                sub="sub 1",
                updated_at="21",
                id_updated_at="name 1#21",
                updated_at_id="21#name 1",
            ),
        ],
        "sub 1",
        "name 1",
        [0, 1],
        id="multiple hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                version="version 1",
                id_updated_at="name 1#11",
                updated_at_id="11#name 1",
            ),
            factory.SpecFactory(
                sub="sub 1",
                updated_at="21",
                version="version 1",
                id_updated_at="name 1#21",
                updated_at_id="21#name 1",
            ),
        ],
        "sub 1",
        "name 1",
        [0, 1],
        id="multiple hit duplicate version",
    ),
]


@pytest.mark.parametrize(
    "items, sub, name, expected_idx_list",
    LIST_VERSIONS_TESTS,
)
@pytest.mark.models
def test_list_versions(items, sub, name, expected_idx_list):
    """
    GIVEN items in the database and sub and spec name
    WHEN list_versions is called on Spec with the sub and spec name
    THEN the expected spec infos are returned.
    """
    for item in items:
        item.save()

    returned_spec_infos = models.Spec.list_versions(sub=sub, name=name)

    expected_spec_info = list(
        map(
            models.Spec.item_to_info,
            map(lambda idx: items[idx], expected_idx_list),
        )
    )
    assert returned_spec_infos == expected_spec_info

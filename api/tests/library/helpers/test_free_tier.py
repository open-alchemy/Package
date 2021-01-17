"""Tests for the free tier helper."""

import pytest
from library import config
from library.helpers import free_tier
from open_alchemy import package_database

CHECK_WITHIN_LIMIT_TESTS = [
    pytest.param(
        [], "user 1", "name 1", 0, True, None, id="empty database no additional"
    ),
    pytest.param(
        [], "user 1", "name 1", 1, True, None, id="empty database some additional"
    ),
    pytest.param(
        [], "user 1", "name 1", 10, True, None, id="empty database equal additional"
    ),
    pytest.param(
        [],
        "user 1",
        "name 1",
        11,
        False,
        ["current", "0", "this spec", "0", "new", "11", "total", "11"],
        id="empty database more than additional",
    ),
    pytest.param(
        [],
        "user 1",
        "name 1",
        15,
        False,
        ["0", "0", "15", "15"],
        id="empty database much more than additional",
    ),
    pytest.param(
        [{"sub": "user 1", "name": "name 1", "version": "version 1", "model_count": 0}],
        "user 1",
        "name 2",
        0,
        True,
        None,
        id="single item no model database no additional",
    ),
    pytest.param(
        [{"sub": "user 1", "name": "name 1", "version": "version 1", "model_count": 5}],
        "user 1",
        "name 2",
        0,
        True,
        None,
        id="single item some model database no additional",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 10,
            }
        ],
        "user 1",
        "name 2",
        0,
        True,
        None,
        id="single item equal model database no additional",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 11,
            }
        ],
        "user 1",
        "name 2",
        0,
        False,
        ["current", "11", "this spec", "0", "new", "0", "total", "11"],
        id="single item more than model database no additional",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 15,
            }
        ],
        "user 1",
        "name 2",
        0,
        False,
        ["current", "15", "this spec", "0", "new", "0", "total", "15"],
        id="single item much more than model database no additional",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 1,
            }
        ],
        "user 1",
        "name 2",
        1,
        True,
        None,
        id="single less than model database less than additional total less",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 5,
            }
        ],
        "user 1",
        "name 2",
        5,
        True,
        None,
        id="single less than model database less than additional total equal",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 5,
            }
        ],
        "user 1",
        "name 2",
        6,
        False,
        ["current", "5", "this spec", "0", "new", "6", "total", "11"],
        id="single less than model database less than additional total more than",
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 5,
            }
        ],
        "user 1",
        "name 1",
        6,
        True,
        None,
        id=(
            "single less than model database less than additional same model "
            "total more than"
        ),
    ),
    pytest.param(
        [
            {
                "sub": "user 1",
                "name": "name 1",
                "version": "version 1",
                "model_count": 5,
            }
        ],
        "user 2",
        "name 2",
        6,
        True,
        None,
        id=(
            "single less than model database less than additional different user "
            "total more than"
        ),
    ),
]


@pytest.mark.parametrize(
    "initial_items, user, spec_name, model_count, expected_result, expected_contents",
    CHECK_WITHIN_LIMIT_TESTS,
)
@pytest.mark.helpers
def test_check_within_limit(
    initial_items,
    user,
    spec_name,
    model_count,
    expected_result,
    expected_contents,
    _clean_specs_table,
):
    """
    GIVE database with initial items, a user, the name of a spec and a model count
    WHEN check_within_limit is called with the user, spec name and model count
    THEN the expected result and reason is returned.
    """
    free_tier_model_count = 10
    config.get().free_tier_model_count = free_tier_model_count
    for item in initial_items:
        package_database.get().create_update_spec(**item)

    returned_result = free_tier.check_within_limit(
        user=user, spec_name=spec_name, model_count=model_count
    )

    assert returned_result.value == expected_result
    if expected_result:
        assert returned_result.reason is None
    else:
        assert str(free_tier_model_count) in returned_result.reason
        for content in expected_contents:
            assert content in returned_result.reason

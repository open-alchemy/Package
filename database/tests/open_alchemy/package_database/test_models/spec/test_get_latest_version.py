"""Tests for the models."""

import pytest
from open_alchemy.package_database import exceptions, factory, models

GET_LATEST_VERSION_NOT_FOUND_TESTS = [
    pytest.param([], "sub 1", "name 1", id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 2",
                name="name 1",
                id="name 1",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#",
            )
        ],
        "sub 1",
        "name 1",
        id="single item sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 2",
                id="name 2",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#",
            )
        ],
        "sub 1",
        "name 1",
        id="single item name miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                updated_at_id="11#",
            )
        ],
        "sub 1",
        "name 1",
        id="single item updated_at_id miss",
    ),
]


@pytest.mark.parametrize("items, sub, name", GET_LATEST_VERSION_NOT_FOUND_TESTS)
@pytest.mark.models
def test_get_latest_version_not_found(items, sub, name):
    """
    GIVEN items in the database and sub and spec name
    WHEN get_latest_version is called on Spec with the sub and spec name
    THEN NotFoundError is raised.
    """
    for item in items:
        item.save()

    with pytest.raises(exceptions.NotFoundError) as exc:
        models.Spec.get_latest_version(sub=sub, name=name)

    assert sub in str(exc)
    assert name in str(exc)


GET_LATEST_VERSION_TESTS = [
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            )
        ],
        "sub 1",
        "name 1",
        "version 1",
        id="single",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="NAME 1",
                id="name 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            )
        ],
        "sub 1",
        "NAME 1",
        "version 1",
        id="single different canonical name",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            ),
            factory.SpecFactory(
                sub="sub 2",
                name="name 2",
                id="name 2",
                version="version 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 2"),
            ),
        ],
        "sub 1",
        "name 1",
        "version 1",
        id="multiple first",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                name="name 1",
                id="name 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 1"),
            ),
            factory.SpecFactory(
                sub="sub 2",
                name="name 2",
                id="name 2",
                version="version 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#name 2"),
            ),
        ],
        "sub 2",
        "name 2",
        "version 2",
        id="multiple second",
    ),
]


@pytest.mark.parametrize(
    "items, sub, name, expected_version",
    GET_LATEST_VERSION_TESTS,
)
@pytest.mark.models
def test_get_latest_version(items, sub, name, expected_version):
    """
    GIVEN items in the database and sub and spec name
    WHEN get_latest_version is called on Spec with the sub and spec name
    THEN the expected version is returned.
    """
    for item in items:
        item.save()

    returned_version = models.Spec.get_latest_version(sub=sub, name=name.lower())

    assert returned_version == expected_version

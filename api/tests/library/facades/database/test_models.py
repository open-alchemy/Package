"""Tests for the models."""

import time

import pytest

from library.facades.database import models

from . import factory

PACKAGE_STORAGE_COUNT_CUSTOMER_MODELS_TESTS = [
    pytest.param([], "sub 2", 0, id="empty"),
    pytest.param(
        [factory.PackageStorageFactory(sub="sub 1")],
        "sub 1",
        0,
        id="single item sub miss",
    ),
    pytest.param(
        [factory.PackageStorageFactory(sub="sub 1", updated_at_spec_id="11#spec 1")],
        "sub 1",
        0,
        id="single item sub hit updated_at miss",
    ),
    pytest.param(
        [
            factory.PackageStorageFactory(
                sub="sub 1",
                updated_at_spec_id=f"{models.PackageStorage.UPDATED_AT_LATEST}#spec 1",
                model_count=12,
            )
        ],
        "sub 1",
        12,
        id="single item sub hit updated_at hit",
    ),
    pytest.param(
        [
            factory.PackageStorageFactory(
                sub="sub 2",
                updated_at_spec_id=f"{models.PackageStorage.UPDATED_AT_LATEST}#spec 2",
                model_count=22,
            )
        ],
        "sub 2",
        22,
        id="single item sub hit updated_at different hit",
    ),
    pytest.param(
        [
            factory.PackageStorageFactory(sub="sub 2"),
            factory.PackageStorageFactory(sub="sub 2"),
        ],
        "sub 1",
        0,
        id="multiple item all miss",
    ),
    pytest.param(
        [
            factory.PackageStorageFactory(
                sub="sub 1",
                updated_at_spec_id=f"{models.PackageStorage.UPDATED_AT_LATEST}#spec 1",
                model_count=12,
            ),
            factory.PackageStorageFactory(sub="sub 2"),
        ],
        "sub 1",
        12,
        id="multiple item first hit",
    ),
    pytest.param(
        [
            factory.PackageStorageFactory(sub="sub 1"),
            factory.PackageStorageFactory(
                sub="sub 2",
                updated_at_spec_id=f"{models.PackageStorage.UPDATED_AT_LATEST}#spec 2",
                model_count=22,
            ),
        ],
        "sub 2",
        22,
        id="multiple item second hit",
    ),
    pytest.param(
        [
            factory.PackageStorageFactory(
                sub="sub 1",
                updated_at_spec_id=f"{models.PackageStorage.UPDATED_AT_LATEST}#spec 1",
                model_count=12,
            ),
            factory.PackageStorageFactory(
                sub="sub 1",
                updated_at_spec_id=f"{models.PackageStorage.UPDATED_AT_LATEST}#spec 2",
                model_count=22,
            ),
        ],
        "sub 1",
        34,
        id="multiple item all hit",
    ),
]


@pytest.mark.parametrize(
    "items, sub, expected_count", PACKAGE_STORAGE_COUNT_CUSTOMER_MODELS_TESTS
)
def test_package_storage_count_customer_models(
    items, sub, expected_count, _clean_package_storage_table
):
    """
    GIVEN items in the database and sub
    WHEN count_customer_models on PackageStorage is called with the sub
    THEN the expected count is returned.
    """
    for item in items:
        item.save()

    returned_count = models.PackageStorage.count_customer_models(sub=sub)

    assert returned_count == expected_count


def test_package_storage_create_update_item_empty(_clean_package_storage_table):
    """
    GIVEN empty database, sub, spec id, version and model count
    WHEN create_update_item is called on PackageStorage with the sub, spec id, version
        and model count
    THEN an item is created with the sub, spec id, version and model count as well as
        updated_at with close to the current time and a correct sort key value
    AND another similar record with updated_at set to latest
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    model_count = 11

    models.PackageStorage.create_update_item(
        sub=sub, spec_id=spec_id, version=version, model_count=model_count
    )

    items = list(
        models.PackageStorage.query(
            sub,
            models.PackageStorage.updated_at_spec_id.startswith(
                f"{str(time.time())[:1]}"
            ),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.sub == sub
    assert item.spec_id == spec_id
    assert item.version == version
    assert isinstance(item.model_count, int)
    assert item.model_count == model_count
    assert not "." in item.updated_at
    assert int(item.updated_at) == pytest.approx(time.time(), abs=10)
    assert item.updated_at_spec_id == f"{item.updated_at}#{item.spec_id}"

    items = list(
        models.PackageStorage.query(
            sub,
            models.PackageStorage.updated_at_spec_id.startswith(
                f"{models.PackageStorage.UPDATED_AT_LATEST}#"
            ),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.sub == sub
    assert item.spec_id == spec_id
    assert item.version == version
    assert isinstance(item.model_count, int)
    assert item.model_count == model_count
    assert item.updated_at == models.PackageStorage.UPDATED_AT_LATEST
    assert item.updated_at_spec_id == f"{item.updated_at}#{item.spec_id}"

    items = list(models.PackageStorage.query(sub))
    assert len(items) == 2

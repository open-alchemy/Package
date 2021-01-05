"""Tests for the models."""

import time
from unittest import mock

import pytest
from open_alchemy.package_database import factory, models
from packaging import utils


@pytest.mark.parametrize(
    "sub, name, version, title, description, model_count",
    [
        pytest.param(
            "sub 1",
            "name 1",
            "version 1",
            None,
            None,
            11,
            id="title description None",
        ),
        pytest.param(
            "sub 1",
            "name 1",
            "version 1",
            "title 1",
            "description 1",
            11,
            id="title description defined",
        ),
    ],
)
@pytest.mark.models
def test_create_update_item_empty(sub, name, version, title, description, model_count):
    """
    GIVEN empty database, sub, spec name, version, title, description and model count
    WHEN create_update_item is called on Spec with the sub, spec name, version
        title, description and model count
    THEN an item is created with the sub, spec name and id, version, title, description
        and model count as well as updated_at with close to the current time and a
        correct sort key value
    AND another similar record with updated_at set to latest
    """
    models.Spec.create_update_item(
        sub=sub,
        name=name,
        version=version,
        title=title,
        description=description,
        model_count=model_count,
    )

    items = list(
        models.Spec.query(
            sub,
            models.Spec.updated_at_id.startswith("0"),
        )
    )
    assert len(items) == 1
    [item] = items
    expected_id = utils.canonicalize_name(name)
    assert item.sub == sub
    assert item.id == expected_id
    assert item.name == name
    assert item.version == version
    assert item.title == title
    assert item.description == description
    assert isinstance(item.model_count, int)
    assert item.model_count == model_count
    assert not "." in item.updated_at
    assert int(item.updated_at) == pytest.approx(time.time(), abs=10)
    expected_updated_at = item.updated_at.zfill(20)
    assert item.updated_at_id == f"{expected_updated_at}#{item.id}"
    assert item.id_updated_at == f"{item.id}#{expected_updated_at}"

    items = list(
        models.Spec.query(
            sub,
            models.Spec.updated_at_id.startswith(f"{models.Spec.UPDATED_AT_LATEST}#"),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.sub == sub
    assert item.id == expected_id
    assert item.name == name
    assert item.version == version
    assert item.title == title
    assert item.description == description
    assert isinstance(item.model_count, int)
    assert item.model_count == model_count
    assert int(item.updated_at) == pytest.approx(time.time(), abs=10)
    assert item.updated_at_id == f"{models.Spec.UPDATED_AT_LATEST}#{item.id}"
    assert item.id_updated_at == f"{item.id}#{models.Spec.UPDATED_AT_LATEST}"

    items = list(models.Spec.scan())
    assert len(items) == 2


@pytest.mark.models
def test_create_update_item_single():
    """
    GIVEN database that has a different record and sub and spec id
    WHEN create_update_item is called on Spec with the sub, spec id
    THEN an new item is created with the sub and spec id and updated_at with the
        current time
    AND another similar record with updated_at set to latest
    """
    initial_item_name = "name 1"
    initial_item = factory.SpecFactory(
        sub="sub 1", name=initial_item_name, id=initial_item_name
    )
    initial_item.save()
    sub = "sub 2"
    name = "name 2"
    version = "version 2"
    model_count = 21

    models.Spec.create_update_item(
        sub=sub, name=name, version=version, model_count=model_count
    )

    items = list(
        models.Spec.query(
            sub,
            (models.Spec.updated_at_id.startswith("0")),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.sub == sub
    assert item.name == name
    assert int(item.updated_at) == pytest.approx(time.time(), abs=10)

    items = list(
        models.Spec.query(
            sub,
            models.Spec.updated_at_id.startswith(f"{models.Spec.UPDATED_AT_LATEST}#"),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.sub == sub
    assert item.name == name
    assert int(item.updated_at) == pytest.approx(time.time(), abs=10)

    items = list(models.Spec.scan())
    assert len(items) == 3


@pytest.mark.models
def test_create_update_item_update(monkeypatch):
    """
    GIVEN empty database a sub and spec id and multiple model count and versions
    WHEN create_update_item is called on Spec multiple times with the same
        sub and spec id but different versions and model counts at different times
    THEN a record for each version is added to the database
    AND the latest record points to the last inserted record.
    """
    sub = "sub 1"
    name_1 = "name 1"
    version_1 = "version 1"
    time_1 = 1000000
    model_count_1 = 11
    version_2 = "version 2"
    model_count_2 = 21
    time_2 = 2000000
    mock_time = mock.MagicMock()
    monkeypatch.setattr(time, "time", mock_time)

    mock_time.return_value = time_1
    models.Spec.create_update_item(
        sub=sub, name=name_1, version=version_1, model_count=model_count_1
    )
    mock_time.return_value = time_2
    models.Spec.create_update_item(
        sub=sub, name=name_1, version=version_2, model_count=model_count_2
    )

    # Check first time
    items = list(
        models.Spec.query(
            sub,
            (models.Spec.updated_at_id.startswith(f"{str(time_1).zfill(20)}#")),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.model_count == model_count_1
    assert item.version == version_1
    assert int(item.updated_at) == time_1

    # Check second time
    items = list(
        models.Spec.query(
            sub,
            (models.Spec.updated_at_id.startswith(f"{str(time_2).zfill(20)}#")),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.model_count == model_count_2
    assert item.version == version_2
    assert int(item.updated_at) == time_2

    items = list(
        models.Spec.query(
            sub,
            models.Spec.updated_at_id.startswith(f"{models.Spec.UPDATED_AT_LATEST}#"),
        )
    )
    assert len(items) == 1
    [item] = items
    assert item.model_count == model_count_2
    assert item.version == version_2

    items = list(models.Spec.scan())
    assert len(items) == 3

    # Call again with different name by same canonical name
    name_2 = "NAME 1"
    models.Spec.create_update_item(
        sub=sub, name=name_2, version=version_2, model_count=model_count_2
    )

    items = list(
        models.Spec.query(
            sub,
            (models.Spec.updated_at_id.startswith(f"{str(time_2).zfill(20)}#")),
        )
    )
    assert len(items) == 1
    [different_item] = items
    assert different_item.name == name_2
    assert different_item.id == item.id
    assert different_item.model_count == model_count_2
    assert different_item.version == version_2
    assert int(different_item.updated_at) == time_2

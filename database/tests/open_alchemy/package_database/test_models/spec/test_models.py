"""Tests for the models."""

import time
from unittest import mock

import pytest
from open_alchemy.package_database import exceptions, factory, models

COUNT_CUSTOMER_MODELS_TESTS = [
    pytest.param([], "sub 2", 0, id="empty"),
    pytest.param(
        [factory.SpecFactory(sub="sub 1")],
        "sub 1",
        0,
        id="single item sub miss",
    ),
    pytest.param(
        [factory.SpecFactory(sub="sub 1", updated_at_id="11#spec 1")],
        "sub 1",
        0,
        id="single item sub hit updated_at miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#spec 1",
                model_count=12,
            )
        ],
        "sub 1",
        12,
        id="single item sub hit updated_at hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 2",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#spec 2",
                model_count=22,
            )
        ],
        "sub 2",
        22,
        id="single item sub hit updated_at different hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 2"),
            factory.SpecFactory(sub="sub 2"),
        ],
        "sub 1",
        0,
        id="multiple item all miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#spec 1",
                model_count=12,
            ),
            factory.SpecFactory(sub="sub 2"),
        ],
        "sub 1",
        12,
        id="multiple item first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(sub="sub 1"),
            factory.SpecFactory(
                sub="sub 2",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#spec 2",
                model_count=22,
            ),
        ],
        "sub 2",
        22,
        id="multiple item second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#spec 1",
                model_count=12,
            ),
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#spec 2",
                model_count=22,
            ),
        ],
        "sub 1",
        34,
        id="multiple item all hit",
    ),
]


@pytest.mark.parametrize("items, sub, expected_count", COUNT_CUSTOMER_MODELS_TESTS)
def test_count_customer_models(items, sub, expected_count):
    """
    GIVEN items in the database and sub
    WHEN count_customer_models on Spec is called with the sub
    THEN the expected count is returned.
    """
    for item in items:
        item.save()

    returned_count = models.Spec.count_customer_models(sub=sub)

    assert returned_count == expected_count


@pytest.mark.parametrize(
    "sub, id_, version, title, description, model_count",
    [
        pytest.param(
            "sub 1",
            "spec id 1",
            "version 1",
            None,
            None,
            11,
            id="title description None",
        ),
        pytest.param(
            "sub 1",
            "spec id 1",
            "version 1",
            "title 1",
            "description 1",
            11,
            id="title description defined",
        ),
    ],
)
def test_create_update_item_empty(sub, id_, version, title, description, model_count):
    """
    GIVEN empty database, sub, spec id, version, title, description and model count
    WHEN create_update_item is called on Spec with the sub, spec id, version
        title, description and model count
    THEN an item is created with the sub, spec id, version, title, description and
        model count as well as updated_at with close to the current time and a correct
        sort key value
    AND another similar record with updated_at set to latest
    """
    models.Spec.create_update_item(
        sub=sub,
        id_=id_,
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
    assert item.sub == sub
    assert item.id == id_
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
    assert item.id == id_
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


def test_create_update_item_single():
    """
    GIVEN database that has a different record and sub and spec id
    WHEN create_update_item is called on Spec with the sub, spec id
    THEN an new item is created with the sub and spec id and updated_at with the
        current time
    AND another similar record with updated_at set to latest
    """
    initial_item = factory.SpecFactory(sub="sub 1", id="spec id 1")
    initial_item.save()
    sub = "sub 2"
    id_ = "spec id 2"
    version = "version 2"
    model_count = 21

    models.Spec.create_update_item(
        sub=sub, id_=id_, version=version, model_count=model_count
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
    assert item.id == id_
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
    assert item.id == id_
    assert int(item.updated_at) == pytest.approx(time.time(), abs=10)

    items = list(models.Spec.scan())
    assert len(items) == 3


def test_create_update_item_update(monkeypatch):
    """
    GIVEN empty database a sub and spec id and multiple model count and versions
    WHEN create_update_item is called on Spec multiple times with the same
        sub and spec id but different versions and model counts at different times
    THEN a record for each version is added to the database
    AND the latest record points to the last inserted record.
    """
    sub = "sub 1"
    id_ = "spec id 1"
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
        sub=sub, id_=id_, version=version_1, model_count=model_count_1
    )
    mock_time.return_value = time_2
    models.Spec.create_update_item(
        sub=sub, id_=id_, version=version_2, model_count=model_count_2
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


GET_LATEST_version_NOT_FOUND_TESTS = [
    pytest.param([], "sub 1", "spec id 1", id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 2",
                id="spec id 1",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#",
            )
        ],
        "sub 1",
        "spec id 1",
        id="single item sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 2",
                updated_at_id=f"{models.Spec.UPDATED_AT_LATEST}#",
            )
        ],
        "sub 1",
        "spec id 1",
        id="single item id miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                updated_at_id="11#",
            )
        ],
        "sub 1",
        "spec id 1",
        id="single item updated_at_id miss",
    ),
]


@pytest.mark.parametrize("items, sub, id_", GET_LATEST_version_NOT_FOUND_TESTS)
def test_get_latest_version_not_found(items, sub, id_):
    """
    GIVEN items in the database and sub and spec id
    WHEN get_latest_version is called on Spec with the sub and spec id
    THEN NotFoundError is raised.
    """
    for item in items:
        item.save()

    with pytest.raises(exceptions.NotFoundError) as exc:
        models.Spec.get_latest_version(sub=sub, id_=id_)

    assert sub in str(exc)
    assert id_ in str(exc)


GET_LATEST_VERSION_TESTS = [
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
            )
        ],
        "sub 1",
        "spec id 1",
        "version 1",
        id="single",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
            ),
            factory.SpecFactory(
                sub="sub 2",
                id="spec id 2",
                version="version 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 2"),
            ),
        ],
        "sub 1",
        "spec id 1",
        "version 1",
        id="multiple first",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                version="version 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
            ),
            factory.SpecFactory(
                sub="sub 2",
                id="spec id 2",
                version="version 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 2"),
            ),
        ],
        "sub 2",
        "spec id 2",
        "version 2",
        id="multiple second",
    ),
]


@pytest.mark.parametrize(
    "items, sub, id_, expected_version",
    GET_LATEST_VERSION_TESTS,
)
def test_get_latest_version(items, sub, id_, expected_version):
    """
    GIVEN items in the database and sub and spec id
    WHEN get_latest_version is called on Spec with the sub and spec id
    THEN the expected version is returned.
    """
    for item in items:
        item.save()

    returned_version = models.Spec.get_latest_version(sub=sub, id_=id_)

    assert returned_version == expected_version


LIST_SPECS_TESTS = [
    pytest.param([], "sub 1", [], id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
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
                id="spec id 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
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
                id="spec id 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
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
                id="spec id 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 2"),
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
                id="spec id 1",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
            ),
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 2",
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 2"),
            ),
        ],
        "sub 1",
        [0, 1],
        id="multiple hit",
    ),
]


@pytest.mark.parametrize("items, sub, expected_idx_list", LIST_SPECS_TESTS)
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


@pytest.mark.parametrize(
    "title, description, expected_spec_info",
    [
        pytest.param(None, None, {}, id="title description not defined"),
        pytest.param(
            "title 1",
            "description 1",
            {
                "title": "title 1",
                "description": "description 1",
            },
            id="title description defined",
        ),
    ],
)
def test_item_to_info(title, description, expected_spec_info):
    """
    GIVEN title and description
    WHEN Spec is constructed with the title and description
    THEN the expected spec info is returned.
    """
    item = factory.SpecFactory(title=title, description=description)
    expected_spec_info["id"] = item.id
    expected_spec_info["version"] = item.version
    expected_spec_info["model_count"] = item.model_count
    expected_spec_info["updated_at"] = int(item.updated_at)

    spec_info = models.Spec.item_to_info(item)

    assert spec_info == expected_spec_info


DELETE_ITEM_TESTS = [
    pytest.param([], "sub 1", "spec id 1", 0, id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            )
        ],
        "sub 2",
        "spec id 1",
        1,
        id="single sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            )
        ],
        "sub 1",
        "spec id 2",
        1,
        id="single id miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            )
        ],
        "sub 1",
        "spec id 1",
        0,
        id="single hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            ),
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#21",
            ),
        ],
        "sub 1",
        "spec id 1",
        0,
        id="multiple hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            ),
            factory.SpecFactory(
                sub="sub 2",
                id="spec id 2",
                id_updated_at="spec id 2#21",
            ),
        ],
        "sub 1",
        "spec id 1",
        1,
        id="multiple first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            ),
            factory.SpecFactory(
                sub="sub 2",
                id="spec id 2",
                id_updated_at="spec id 2#21",
            ),
        ],
        "sub 2",
        "spec id 2",
        1,
        id="multiple second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                id="spec id 1",
                id_updated_at="spec id 1#11",
            ),
            factory.SpecFactory(
                sub="sub 2",
                id="spec id 2",
                id_updated_at="spec id 2#21",
            ),
        ],
        "sub 3",
        "spec id 3",
        2,
        id="multiple miss",
    ),
]


@pytest.mark.parametrize("items, sub, id_, expected_item_count", DELETE_ITEM_TESTS)
def test_delete_item(items, sub, id_, expected_item_count):
    """
    GIVEN items in the database and sub and spec id
    WHEN delete_item is called on Spec with the sub and spec id
    THEN the expected number of items in the database remain.
    """
    for item in items:
        item.save()

    models.Spec.delete_item(sub=sub, id_=id_)

    assert len(list(models.Spec.scan())) == expected_item_count


LIST_VERSIONS_TESTS = [
    pytest.param([], "sub 1", "spec id 1", [], id="empty"),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            )
        ],
        "sub 2",
        "spec id 1",
        [],
        id="single sub miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            )
        ],
        "sub 1",
        "spec id 2",
        [],
        id="single spec id miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at=(f"spec id 1#{models.Spec.UPDATED_AT_LATEST}"),
                updated_at_id=(f"{models.Spec.UPDATED_AT_LATEST}#spec id 1"),
            )
        ],
        "sub 1",
        "spec id 1",
        [],
        id="single updated at miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            )
        ],
        "sub 1",
        "spec id 1",
        [0],
        id="single hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            ),
            factory.SpecFactory(
                sub="sub 2",
                updated_at="21",
                id_updated_at="spec id 2#21",
                updated_at_id="21#spec id 2",
            ),
        ],
        "sub 3",
        "spec id 3",
        [],
        id="multiple miss",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            ),
            factory.SpecFactory(
                sub="sub 2",
                updated_at="21",
                id_updated_at="spec id 2#21",
                updated_at_id="21#spec id 2",
            ),
        ],
        "sub 1",
        "spec id 1",
        [0],
        id="multiple first hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            ),
            factory.SpecFactory(
                sub="sub 2",
                updated_at="21",
                id_updated_at="spec id 2#21",
                updated_at_id="21#spec id 2",
            ),
        ],
        "sub 2",
        "spec id 2",
        [1],
        id="multiple second hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            ),
            factory.SpecFactory(
                sub="sub 1",
                updated_at="21",
                id_updated_at="spec id 1#21",
                updated_at_id="21#spec id 1",
            ),
        ],
        "sub 1",
        "spec id 1",
        [0, 1],
        id="multiple hit",
    ),
    pytest.param(
        [
            factory.SpecFactory(
                sub="sub 1",
                updated_at="11",
                version="version 1",
                id_updated_at="spec id 1#11",
                updated_at_id="11#spec id 1",
            ),
            factory.SpecFactory(
                sub="sub 1",
                updated_at="21",
                version="version 1",
                id_updated_at="spec id 1#21",
                updated_at_id="21#spec id 1",
            ),
        ],
        "sub 1",
        "spec id 1",
        [0, 1],
        id="multiple hit duplicate version",
    ),
]


@pytest.mark.parametrize(
    "items, sub, id_, expected_idx_list",
    LIST_VERSIONS_TESTS,
)
def test_list_versions(items, sub, id_, expected_idx_list):
    """
    GIVEN items in the database and sub and spec id
    WHEN list_versions is called on Spec with the sub and spec id
    THEN the expected spec ids are returned.
    """
    for item in items:
        item.save()

    returned_spec_infos = models.Spec.list_versions(sub=sub, id_=id_)

    expected_spec_info = list(
        map(
            models.Spec.item_to_info,
            map(lambda idx: items[idx], expected_idx_list),
        )
    )
    assert returned_spec_infos == expected_spec_info


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
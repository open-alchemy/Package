"""Tests for database facade."""

import time
from unittest import mock

import pytest
from open_alchemy import package_database


def test_count_customer_models(_clean_spec_table):
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and count_customer_models is
        called
    THEN the model count is returned.
    """
    sub = "sub 1"
    database_instance = package_database.get()

    assert database_instance.count_customer_models(sub=sub) == 0

    id_ = "spec id 1"
    version = "version 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version, model_count=model_count_1
    )

    assert database_instance.count_customer_models(sub=sub) == model_count_1

    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version, model_count=model_count_2
    )

    assert database_instance.count_customer_models(sub=sub) == model_count_2

    assert database_instance.count_customer_models(sub="sub 2") == 0


@pytest.mark.parametrize(
    "initial_count, additional_count, expected_result",
    [
        pytest.param(0, 0, False, id="zero initial count, zero additional"),
        pytest.param(
            0, 9, False, id="zero initial count, just less than limit additional"
        ),
        pytest.param(0, 10, False, id="zero initial count, equal to limit additional"),
        pytest.param(
            0, 11, True, id="zero initial count, just more than limit additional"
        ),
        pytest.param(0, 15, True, id="zero initial count, more than limit additional"),
        pytest.param(
            9, 0, False, id="just less than limit initial count, zero additional"
        ),
        pytest.param(10, 0, False, id="equal to limit initial count, zero additional"),
        pytest.param(
            11, 0, True, id="just more than limit initial count, zero additional"
        ),
        pytest.param(15, 0, True, id="more than limit initial count, zero additional"),
        pytest.param(
            5, 4, False, id="sum of initial and additional just less than limit"
        ),
        pytest.param(5, 5, False, id="sum of initial and additional equal to limit"),
        pytest.param(
            5, 6, True, id="sum of initial and additional just more than limit"
        ),
    ],
)
def test_check_would_exceed_free_tier(
    initial_count, additional_count, expected_result, _clean_spec_table
):
    """
    GIVEN initial count and additional count
    WHEN create_update_spec is called with the initial count and
        check_would_exceed_free_tier with the additional count
    THEN the expected result is returned
    """
    sub = "sub 1"
    id_ = "spec id 1"
    version = "version 1"
    database_instance = package_database.get()

    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version, model_count=initial_count
    )

    returned_result = database_instance.check_would_exceed_free_tier(
        sub=sub, model_count=additional_count
    )

    assert returned_result.result == expected_result


def test_get_latest_spec_version(_clean_spec_table):
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and get_latest_spec_version is
        called
    THEN the latest version is returned.
    """
    sub = "sub 1"
    id_ = "spec id 1"
    database_instance = package_database.get()

    with pytest.raises(package_database.exceptions.BaseError):
        database_instance.get_latest_spec_version(sub=sub, id_=id_)

    version_1 = "version 1"
    model_count = 1
    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version_1, model_count=model_count
    )

    assert database_instance.get_latest_spec_version(sub=sub, id_=id_) == version_1

    version_2 = "version 2"
    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version_2, model_count=model_count
    )

    assert database_instance.get_latest_spec_version(sub=sub, id_=id_) == version_2

    with pytest.raises(package_database.exceptions.BaseError):
        database_instance.get_latest_spec_version(sub=sub, id_="spec id 2")

    with pytest.raises(package_database.exceptions.BaseError):
        database_instance.get_latest_spec_version(sub="sub 2", id_=id_)


def test_list_specs(_clean_spec_table):
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and list_specs is called
    THEN all specs for the customer are returned.
    """
    sub = "sub 1"
    database_instance = package_database.get()

    assert database_instance.list_specs(sub=sub) == []

    id_1 = "spec id 1"
    version_1 = "version 1"
    title = "title 1"
    description = "description 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub,
        id_=id_1,
        version=version_1,
        model_count=model_count_1,
        title=title,
        description=description,
    )

    spec_infos = database_instance.list_specs(sub=sub)
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["id"] == id_1
    assert spec_info["version"] == version_1
    assert spec_info["title"] == title
    assert spec_info["description"] == description
    assert spec_info["model_count"] == model_count_1
    assert "updated_at" in spec_info

    id_2 = "spec id 2"
    version_2 = "version 2"
    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, id_=id_2, version=version_2, model_count=model_count_2
    )

    spec_infos = database_instance.list_specs(sub=sub)
    assert len(spec_infos) == 2
    assert spec_infos[0]["id"] == id_1
    spec_info = spec_infos[1]
    assert spec_info["id"] == id_2
    assert spec_info["version"] == version_2
    assert spec_info["model_count"] == model_count_2
    assert "updated_at" in spec_info


def test_delete_specs(_clean_spec_table):
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and delete_spec is called
    THEN the spec is deleted.
    """
    sub = "sub 1"
    id_ = "spec id 1"
    version = "version 1"
    model_count = 1
    database_instance = package_database.get()
    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version, model_count=model_count
    )

    assert len(database_instance.list_specs(sub=sub)) == 1
    assert database_instance.count_customer_models(sub=sub) == model_count
    assert database_instance.get_latest_spec_version(sub=sub, id_=id_) == version

    database_instance.delete_spec(sub=sub, id_=id_)

    assert len(database_instance.list_specs(sub=sub)) == 0
    assert database_instance.count_customer_models(sub=sub) == 0
    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.get_latest_spec_version(sub=sub, id_=id_)


def test_list_spec_versions(monkeypatch, _clean_spec_table):
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and list_spec_versions is
        called
    THEN all specs for the customer are returned or NotFoundError is raised.
    """
    mock_time = mock.MagicMock()
    monkeypatch.setattr(time, "time", mock_time)
    sub = "sub 1"
    id_ = "spec id 1"
    database_instance = package_database.get()

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.list_spec_versions(sub=sub, id_=id_)

    mock_time.return_value = 1000000
    version_1 = "version 1"
    title = "title 1"
    description = "description 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub,
        id_=id_,
        version=version_1,
        model_count=model_count_1,
        title=title,
        description=description,
    )

    spec_infos = database_instance.list_spec_versions(sub=sub, id_=id_)
    assert len(spec_infos) == 1
    spec_info = spec_infos[0]
    assert spec_info["id"] == id_
    assert spec_info["version"] == version_1
    assert spec_info["title"] == title
    assert spec_info["description"] == description
    assert spec_info["model_count"] == model_count_1
    assert "updated_at" in spec_info

    mock_time.return_value = 2000000
    version_2 = "version 2"
    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, id_=id_, version=version_2, model_count=model_count_2
    )

    spec_infos = database_instance.list_spec_versions(sub=sub, id_=id_)
    assert len(spec_infos) == 2
    assert spec_infos[0]["id"] == id_
    spec_info = spec_infos[1]
    assert spec_info["id"] == id_
    assert spec_info["version"] == version_2
    assert spec_info["model_count"] == model_count_2
    assert "updated_at" in spec_info

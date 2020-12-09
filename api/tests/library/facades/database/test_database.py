"""Tests for database facade."""

import pytest

from library.facades import database


def test_count_customer_models():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and count_customer_models is
        called
    THEN the model count is returned.
    """
    sub = "sub 1"
    database_instance = database.get_database()

    assert database_instance.count_customer_models(sub=sub) == 0

    spec_id = "spec id 1"
    version = "version 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id, version=version, model_count=model_count_1
    )

    assert database_instance.count_customer_models(sub=sub) == model_count_1

    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id, version=version, model_count=model_count_2
    )

    assert database_instance.count_customer_models(sub=sub) == model_count_2

    assert database_instance.count_customer_models(sub="sub 2") == 0


@pytest.mark.parametrize(
    "initial_count, additional_count, expected_result",
    [
        pytest.param(0, 0, False, id="zero initial count, zero additional"),
        pytest.param(
            0, 99, False, id="zero initial count, just less than limit additional"
        ),
        pytest.param(0, 100, False, id="zero initial count, equal to limit additional"),
        pytest.param(
            0, 101, True, id="zero initial count, just more than limit additional"
        ),
        pytest.param(0, 150, True, id="zero initial count, more than limit additional"),
        pytest.param(
            99, 0, False, id="just less than limit initial count, zero additional"
        ),
        pytest.param(100, 0, False, id="equal to limit initial count, zero additional"),
        pytest.param(
            101, 0, True, id="just more than limit initial count, zero additional"
        ),
        pytest.param(150, 0, True, id="more than limit initial count, zero additional"),
        pytest.param(
            50, 49, False, id="sum of initial and additional just less than limit"
        ),
        pytest.param(50, 50, False, id="sum of initial and additional equal to limit"),
        pytest.param(
            50, 51, True, id="sum of initial and additional just more than limit"
        ),
    ],
)
def test_check_would_exceed_free_tier(initial_count, additional_count, expected_result):
    """
    GIVEN initial count and additional count
    WHEN create_update_spec is called with the initial count and
        check_would_exceed_free_tier with the additional count
    THEN the expected result is returned
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    database_instance = database.get_database()

    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id, version=version, model_count=initial_count
    )

    returned_result = database_instance.check_would_exceed_free_tier(
        sub=sub, model_count=additional_count
    )

    assert returned_result.result == expected_result


def test_get_latest_spec_version():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and get_latest_spec_version is
        called
    THEN the latest version is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    database_instance = database.get_database()

    with pytest.raises(database.exceptions.DatabaseError):
        database_instance.get_latest_spec_version(sub=sub, spec_id=spec_id)

    version_1 = "version 1"
    model_count = 1
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id, version=version_1, model_count=model_count
    )

    assert (
        database_instance.get_latest_spec_version(sub=sub, spec_id=spec_id) == version_1
    )

    version_2 = "version 2"
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id, version=version_2, model_count=model_count
    )

    assert (
        database_instance.get_latest_spec_version(sub=sub, spec_id=spec_id) == version_2
    )

    with pytest.raises(database.exceptions.DatabaseError):
        database_instance.get_latest_spec_version(sub=sub, spec_id="spec id 2")

    with pytest.raises(database.exceptions.DatabaseError):
        database_instance.get_latest_spec_version(sub="sub 2", spec_id=spec_id)


def test_list_specs():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and list_specs is called
    THEN all specs for the customer are returned.
    """
    sub = "sub 1"
    database_instance = database.get_database()

    assert database_instance.list_specs(sub=sub) == []

    spec_id_1 = "spec id 1"
    version_1 = "version 1"
    title = "title 1"
    description = "description 1"
    model_count_1 = 1
    database_instance.create_update_spec(
        sub=sub,
        spec_id=spec_id_1,
        version=version_1,
        model_count=model_count_1,
        title=title,
        description=description,
    )

    spec_infos = database_instance.list_specs(sub=sub)
    assert len(spec_infos) == 1
    assert spec_infos == [
        {
            "spec_id": spec_id_1,
            "version": version_1,
            "title": title,
            "description": description,
            "model_count": model_count_1,
        }
    ]

    spec_id_2 = "spec id 2"
    version_2 = "version 2"
    model_count_2 = 2
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id_2, version=version_2, model_count=model_count_2
    )

    spec_infos = database_instance.list_specs(sub=sub)
    assert len(spec_infos) == 2
    assert spec_infos[0]["spec_id"] == spec_id_1
    assert spec_infos[1] == {
        "spec_id": spec_id_2,
        "version": version_2,
        "model_count": model_count_2,
    }


def test_delete_specs():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and delete_spec is called
    THEN the spec is deleted.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    version = "version 1"
    model_count = 1
    database_instance = database.get_database()
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id, version=version, model_count=model_count
    )

    assert len(database_instance.list_specs(sub=sub)) == 1
    assert database_instance.count_customer_models(sub=sub) == model_count
    assert (
        database_instance.get_latest_spec_version(sub=sub, spec_id=spec_id) == version
    )

    database_instance.delete_spec(sub=sub, spec_id=spec_id)

    assert len(database_instance.list_specs(sub=sub)) == 0
    assert database_instance.count_customer_models(sub=sub) == 0
    with pytest.raises(database.exceptions.NotFoundError):
        database_instance.get_latest_spec_version(sub=sub, spec_id=spec_id)

"""Tests for DynamoDB database facade."""

import pytest

from library.facades.database import dynamodb, exceptions


def test_count_customer_models():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and count_customer_models is
        called
    THEN the model count is returned.
    """
    sub = "sub 1"
    database_instance = dynamodb.Database()

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


def test_get_latest_spec_version():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and get_latest_spec_version is
        called
    THEN the latest version is returned.
    """
    sub = "sub 1"
    spec_id = "spec id 1"
    database_instance = dynamodb.Database()

    with pytest.raises(exceptions.BaseError):
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

    with pytest.raises(exceptions.BaseError):
        database_instance.get_latest_spec_version(sub=sub, spec_id="spec id 2")

    with pytest.raises(exceptions.BaseError):
        database_instance.get_latest_spec_version(sub="sub 2", spec_id=spec_id)


def test_list_specs():
    """
    GIVEN sub, spec id, version and model count
    WHEN create_update_spec is called with the spec info and list_specs is called
    THEN all specs for the customer are returned.
    """
    sub = "sub 1"
    database_instance = dynamodb.Database()

    assert database_instance.list_specs(sub=sub) == []

    spec_id_1 = "spec id 1"
    version = "version 1"
    model_count = 1
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id_1, version=version, model_count=model_count
    )

    assert database_instance.list_specs(sub=sub) == [spec_id_1]

    spec_id_2 = "spec id 2"
    database_instance.create_update_spec(
        sub=sub, spec_id=spec_id_2, version=version, model_count=model_count
    )

    assert database_instance.list_specs(sub=sub) == [spec_id_1, spec_id_2]

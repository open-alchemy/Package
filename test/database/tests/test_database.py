"""Database production tests."""

import pytest
from open_alchemy import package_database


def test_spec_create_list_delete_all(sub):
    """
    GIVEN spec values
    WHEN spec is created, listed and all are deleted
    THEN the spec is returned in the list after creation but not after deletion.
    """
    id_ = "id 1"
    model_count = 1
    version = "version 1"
    title = "title 1"
    description = "description 1"

    database_instance = package_database.get()

    assert len(database_instance.list_specs(sub=sub)) == 0

    database_instance.create_update_spec(
        sub=sub,
        id_=id_,
        model_count=model_count,
        version=version,
        title=title,
        description=description,
    )

    assert len(database_instance.list_specs(sub=sub)) == 1

    database_instance.delete_all_specs(sub=sub)

    assert len(database_instance.list_specs(sub=sub)) == 0


def test_spec_create_count_models_get_latest_version_list_versions_delete(sub):
    """
    GIVEN spec values
    WHEN the models are counted, the latest version is retrieved, versions are listed
        and deleted
    THEN the model count for the spec is returned, the version of the spec is returned,
        the version of the spec is listed after creation but not after deletion.
    """
    id_ = "id 1"
    model_count = 1
    version = "version 1"
    title = "title 1"
    description = "description 1"

    database_instance = package_database.get()

    assert len(database_instance.list_specs(sub=sub)) == 0

    database_instance.create_update_spec(
        sub=sub,
        id_=id_,
        model_count=model_count,
        version=version,
        title=title,
        description=description,
    )

    assert database_instance.count_customer_models(sub=sub) == model_count

    assert (
        database_instance.check_would_exceed_free_tier(sub=sub, model_count=0).result
        is False
    )
    assert (
        database_instance.check_would_exceed_free_tier(sub=sub, model_count=1000).result
        is True
    )

    assert database_instance.get_latest_spec_version(sub=sub, id_=id_) == version

    assert database_instance.list_spec_versions(sub=sub, id_=id_) == [version]

    database_instance.delete_spec(sub=sub, id_=id_)

    assert database_instance.count_customer_models(sub=sub) == 0

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.get_latest_spec_version(sub=sub, id_=id_)

    with pytest.raises(package_database.exceptions.NotFoundError):
        database_instance.list_spec_versions(sub=sub, id_=id_)

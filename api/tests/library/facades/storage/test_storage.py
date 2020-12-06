"""Tests for the storage facade."""

import pytest

from library.facades import storage


def test_get_spec():
    """
    GIVEN user, spec id, version and spec str
    WHEN create_update_spec is called with the user, spec id, version and spec str and
        then get_spec is called with the user and spec id
    THEN the spec str is returned or ObjectNotFoundError is raised.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version_1 = "version 1"
    spec_str_1 = "spec str 1"

    storage_instance = storage.get_storage_facade()

    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_1, spec_str=spec_str_1
    )

    assert (
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_1)
        == spec_str_1
    )

    spec_str_2 = "spec str 2"
    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_1, spec_str=spec_str_2
    )

    assert (
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_1)
        == spec_str_2
    )

    version_2 = "version 2"

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_2)

    spec_str_3 = "spec str 3"
    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_2, spec_str=spec_str_3
    )

    assert (
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_2)
        == spec_str_3
    )


def test_delete_spec():
    """
    GIVEN user, spec id, version and spec str
    WHEN create_update_spec is called with the user, spec id, version and spec str and
        then delete_spec is called with the user and spec id
    THEN the spec str is returned or ObjectNotFoundError is raised.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version_1 = "version 1"
    spec_str = "spec str 1"

    storage_instance = storage.get_storage_facade()

    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_1, spec_str=spec_str
    )

    storage_instance.delete_spec(user=user, spec_id=spec_id)

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_1)

    with pytest.raises(storage.exceptions.StorageError):
        storage_instance.delete_spec(user=user, spec_id=spec_id)

    version_2 = "version 2"
    version_3 = "version 3"
    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_2, spec_str=spec_str
    )
    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_3, spec_str=spec_str
    )

    storage_instance.delete_spec(user=user, spec_id=spec_id)

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_2)
    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, spec_id=spec_id, version=version_3)


def test_get_spec_versions():
    """
    GIVEN user, spec id, version and spec str
    WHEN create_update_spec is called with the user, spec id, version and spec str and
        then get_spec_versions is called with the user and spec id
    THEN the version is returned or ObjectNotFoundError is raised.
    """
    user = "user 1"
    spec_id = "spec id 1"
    version_1 = "version 1"
    spec_str = "spec str 1"

    storage_instance = storage.get_storage_facade()

    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_1, spec_str=spec_str
    )

    assert storage_instance.get_spec_versions(user=user, spec_id=spec_id) == [version_1]

    version_2 = "version 2"

    storage_instance.create_update_spec(
        user=user, spec_id=spec_id, version=version_2, spec_str=spec_str
    )

    assert (
        storage_instance.get_spec_versions(
            user=user,
            spec_id=spec_id,
        )
        == [version_1, version_2]
    )

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.get_spec_versions(user="user 2", spec_id=spec_id)
    assert spec_id in str(exc)

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.get_spec_versions(user=user, spec_id="spec id 2")
    assert "spec id 2" in str(exc)

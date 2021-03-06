"""Tests for the storage facade."""

import pytest
from library.facades import storage


@pytest.mark.storage
def test_get_spec():
    """
    GIVEN user, name, version and spec str
    WHEN create_update_spec is called with the user, canonically identical name, version
        and spec str and
        then get_spec is called with the user and name
    THEN the spec str is returned or ObjectNotFoundError is raised.
    """
    user = "user 1"
    name = "name 1"
    version_1 = "version 1"
    spec_str_1 = "spec str 1"

    storage_instance = storage.get_storage_facade()

    storage_instance.create_update_spec(
        user=user, name=name, version=version_1, spec_str=spec_str_1
    )

    assert (
        storage_instance.get_spec(user=user, name=name, version=version_1) == spec_str_1
    )
    # Retry with a different name that resolves to the same canonical name
    assert (
        storage_instance.get_spec(user=user, name=name.upper(), version=version_1)
        == spec_str_1
    )

    spec_str_2 = "spec str 2"
    storage_instance.create_update_spec(
        user=user, name=name, version=version_1, spec_str=spec_str_2
    )

    assert (
        storage_instance.get_spec(user=user, name=name, version=version_1) == spec_str_2
    )

    version_2 = "version 2"

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, name=name, version=version_2)

    spec_str_3 = "spec str 3"
    storage_instance.create_update_spec(
        user=user, name=name, version=version_2, spec_str=spec_str_3
    )

    assert (
        storage_instance.get_spec(user=user, name=name, version=version_2) == spec_str_3
    )

    # Update using a a different name that resolves to the same canonical name
    spec_str_4 = "spec str 4"
    storage_instance.create_update_spec(
        user=user, name=name.upper(), version=version_2, spec_str=spec_str_4
    )

    assert (
        storage_instance.get_spec(user=user, name=name, version=version_2) == spec_str_4
    )


@pytest.mark.storage
def test_delete_spec():
    """
    GIVEN user, name, version and spec str
    WHEN create_update_spec is called with the user, canonically identical name,
        version and spec str and then delete_spec is called with the user and name
    THEN the spec str is returned or ObjectNotFoundError is raised.
    """
    user = "user 1"
    name = "name 1"
    version_1 = "version 1"
    spec_str = "spec str 1"

    storage_instance = storage.get_storage_facade()

    storage_instance.create_update_spec(
        user=user, name=name, version=version_1, spec_str=spec_str
    )

    storage_instance.delete_spec(user=user, name=name)

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, name=name, version=version_1)

    # Try again where delete is called with a different name that resolves to the same
    # canonical name
    storage_instance.create_update_spec(
        user=user, name=name, version=version_1, spec_str=spec_str
    )

    storage_instance.delete_spec(user=user, name=name.upper())

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, name=name, version=version_1)

    with pytest.raises(storage.exceptions.StorageError):
        storage_instance.delete_spec(user=user, name=name)

    version_2 = "version 2"
    version_3 = "version 3"
    storage_instance.create_update_spec(
        user=user, name=name, version=version_2, spec_str=spec_str
    )
    storage_instance.create_update_spec(
        user=user, name=name, version=version_3, spec_str=spec_str
    )

    storage_instance.delete_spec(user=user, name=name)

    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, name=name, version=version_2)
    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get_spec(user=user, name=name, version=version_3)


@pytest.mark.storage
def test_get_spec_versions():
    """
    GIVEN user, name, version and spec str
    WHEN create_update_spec is called with the user, canonically identical name, version
        and spec str and then get_spec_versions is called with the user and name
    THEN the version is returned or ObjectNotFoundError is raised.
    """
    user = "user 1"
    name = "name 1"
    version_1 = "version 1"
    spec_str = "spec str 1"

    storage_instance = storage.get_storage_facade()

    storage_instance.create_update_spec(
        user=user, name=name, version=version_1, spec_str=spec_str
    )

    assert storage_instance.get_spec_versions(user=user, name=name) == [version_1]
    assert storage_instance.get_spec_versions(user=user, name=name.upper()) == [
        version_1
    ]

    storage.get_storage().set(key=f"{user}/{name}/{version_1}.gzip", value="value 1")

    assert storage_instance.get_spec_versions(user=user, name=name) == [version_1]

    version_2 = "version 2"

    storage_instance.create_update_spec(
        user=user, name=name, version=version_2, spec_str=spec_str
    )

    assert (
        storage_instance.get_spec_versions(
            user=user,
            name=name,
        )
        == [version_1, version_2]
    )

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.get_spec_versions(user="user 2", name=name)
    assert name in str(exc)

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.get_spec_versions(user=user, name="name 2")
    assert "name 2" in str(exc)

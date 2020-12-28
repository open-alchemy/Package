"""tests for memory torage facade."""

import pytest
from library.facades import storage

CLASSES = [pytest.param(storage.memory.Storage, id="memory")]


@pytest.mark.parametrize("class_", CLASSES)
def test_get_no_set(class_):
    """
    GIVEN storage class
    WHEN it is constructed and get is called
    THEN ObjectNotFoundError is raised.
    """
    key = "key 1"
    storage_instance = class_()

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.get(key=key)

    assert key in str(exc)


@pytest.mark.parametrize("class_", CLASSES)
def test_set_get(class_):
    """
    GIVEN storage class
    WHEN it is constructed and set and then get is called
    THEN the value that set was called with is returned.
    """
    key = "key 1"
    value = "value 1"
    storage_instance = class_()

    storage_instance.set(key=key, value=value)
    returned_value = storage_instance.get(key=key)

    assert returned_value == value


@pytest.mark.parametrize("class_", CLASSES)
def test_delete_no_set(class_):
    """
    GIVEN storage class
    WHEN it is constructed and delete is called
    THEN ObjectNotFoundError is raised.
    """
    key = "key 1"
    storage_instance = class_()

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.delete(key=key)

    assert key in str(exc)


@pytest.mark.parametrize("class_", CLASSES)
def test_set_delete_get(class_):
    """
    GIVEN storage class
    WHEN it is constructed and set, delete and then get is called
    THEN ObjectNotFoundError is raised.
    """
    key = "key 1"
    value = "value 1"
    storage_instance = class_()

    storage_instance.set(key=key, value=value)
    storage_instance.delete(key=key)
    with pytest.raises(storage.exceptions.ObjectNotFoundError):
        storage_instance.get(key=key)


LIST_TESTS = [
    pytest.param([], None, None, [], id="no objects"),
    pytest.param([("key 1", "value 1")], None, None, ["key 1"], id="single objects"),
    pytest.param(
        [("key 1", "value 1")],
        "key 1",
        None,
        ["key 1"],
        id="single objects prefix full hit",
    ),
    pytest.param(
        [("key 1", "value 1")],
        "key",
        None,
        ["key 1"],
        id="single objects prefix partial hit",
    ),
    pytest.param(
        [("key 1", "value 1")], "key 2", None, [], id="single objects prefix miss"
    ),
    pytest.param(
        [("key 1", "value 1")],
        None,
        "key 1",
        ["key 1"],
        id="single objects postfix full hit",
    ),
    pytest.param(
        [("key 1", "value 1")],
        None,
        " 1",
        ["key 1"],
        id="single objects postfix partial hit",
    ),
    pytest.param(
        [("key 1", "value 1")], None, "key 2", [], id="single objects postfix miss"
    ),
    pytest.param(
        [("key 1", "value 1")],
        "key",
        "2",
        [],
        id="single objects prefix hit postfix miss",
    ),
    pytest.param(
        [("key 1", "value 1")],
        "value",
        "1",
        [],
        id="single objects prefix miss postfix hit",
    ),
    pytest.param(
        [("key 1", "value 1")],
        "key",
        "1",
        ["key 1"],
        id="single objects prefix hit postfix hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        None,
        None,
        ["key 1", "key 2"],
        id="multiple objects",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        "key",
        None,
        ["key 1", "key 2"],
        id="multiple objects prefix all hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        "key 1",
        None,
        ["key 1"],
        id="multiple objects prefix first hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        "key 2",
        None,
        ["key 2"],
        id="multiple objects prefix second hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        "key 3",
        None,
        [],
        id="multiple objects prefix no hit",
    ),
    pytest.param(
        [("a key 1", "value 1"), ("b key 1", "value 2")],
        None,
        " 1",
        ["a key 1", "b key 1"],
        id="multiple objects postfix all hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        None,
        "key 1",
        ["key 1"],
        id="multiple objects postfix first hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        None,
        "key 2",
        ["key 2"],
        id="multiple objects postfix second hit",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        None,
        "key 3",
        [],
        id="multiple objects postfix no hit",
    ),
]


@pytest.mark.parametrize("class_", CLASSES)
@pytest.mark.parametrize("set_args, prefix, suffix, expected_keys", LIST_TESTS)
def test_list(class_, set_args, prefix, suffix, expected_keys):
    """
    GIVEN storage class, set args and prefix and suffix
    WHEN it is constructed, set is called with the args and list is called
    THEN the expected keys are returned.
    """
    storage_instance = class_()
    for key, value in set_args:
        storage_instance.set(key=key, value=value)

    returned_keys = storage_instance.list(prefix=prefix, suffix=suffix)

    assert returned_keys == expected_keys


@pytest.mark.parametrize("class_", CLASSES)
def test_delete_all_no_set(class_):
    """
    GIVEN storage class
    WHEN it is constructed and delete_all is called
    THEN ObjectNotFoundError is raised.
    """
    key = "key 1"
    storage_instance = class_()

    with pytest.raises(storage.exceptions.ObjectNotFoundError) as exc:
        storage_instance.delete_all(keys=[key])

    assert key in str(exc)


DELETE_ALL_TESTS = [
    pytest.param([], [], [], id="no objects"),
    pytest.param(
        [("key 1", "value 1")], [], ["key 1"], id="single objects delete none"
    ),
    pytest.param([("key 1", "value 1")], ["key 1"], [], id="single objects delete one"),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        [],
        ["key 1", "key 2"],
        id="multiple objects delete none",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        ["key 1"],
        ["key 2"],
        id="multiple objects delete first",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        ["key 2"],
        ["key 1"],
        id="multiple objects delete second",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        ["key 1", "key 2"],
        [],
        id="multiple objects delete all",
    ),
    pytest.param(
        [("key 1", "value 1"), ("key 2", "value 2")],
        ["key 2", "key 1"],
        [],
        id="multiple objects delete all different order",
    ),
]


@pytest.mark.parametrize("class_", CLASSES)
@pytest.mark.parametrize("set_args, delete_keys, expected_keys", DELETE_ALL_TESTS)
def test_delete_all(class_, set_args, delete_keys, expected_keys):
    """
    GIVEN storage class, set args and keys to delete
    WHEN it is constructed, set is called with the args and delete_all is called with
        the keys to delete and list is called
    THEN the expected keys are returned.
    """
    storage_instance = class_()
    for key, value in set_args:
        storage_instance.set(key=key, value=value)

    returned_keys = storage_instance.delete_all(keys=delete_keys)
    returned_keys = storage_instance.list()

    assert returned_keys == expected_keys

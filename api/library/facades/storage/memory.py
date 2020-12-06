"""Memory implementation for the storage facade."""

import typing

from . import exceptions, types


class Storage:
    """Interface for memory storage."""

    def __init__(self) -> None:
        """Construct."""
        self.storage: typing.Dict[types.TKey, types.TValue] = {}

    def list(
        self,
        prefix: typing.Optional[types.TPrefix] = None,
        suffix: typing.Optional[types.TSuffix] = None,
    ) -> types.TKeys:
        """
        List available objects.

        Args:
            prefix: The prefix any keys must match.
            suffix: The suffix any keys must match.

        Returns:
            All keys that match the prefix and suffix if they were supplied.

        """
        all_keys = self.storage.keys()
        prefix_match_keys = filter(
            lambda key: prefix is None or key.startswith(prefix), all_keys
        )
        prefix_suffix_match_keys = filter(
            lambda key: suffix is None or key.endswith(suffix), prefix_match_keys
        )
        return list(prefix_suffix_match_keys)

    def _check_exists(self, key: types.TKey) -> None:
        """
        Check whether a key exists.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object.

        """
        if key not in self.storage:
            raise exceptions.ObjectNotFoundError(f"could not find object at key {key}")

    def get(self, *, key: types.TKey) -> types.TValue:
        """
        Get a seed by key.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object.

        Returns:
            The value of the object.

        """
        self._check_exists(key)
        return self.storage[key]

    def set(self, *, key: types.TKey, value: types.TValue) -> None:
        """
        Set the object at a key to a value.

        Args:
            key: The key to the object.
            value: The value to set the object to.

        """
        self.storage[key] = value

    def delete(self, *, key: types.TKey) -> None:
        """
        Delete an object by key.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object to delete.

        """
        self._check_exists(key)
        del self.storage[key]

    def delete_all(self, *, keys: types.TKeys) -> None:
        """
        Delete the objects behind the keys.

        Args:
            keys: The keys of the objects to delete.

        """
        for key in keys:
            self.delete(key=key)

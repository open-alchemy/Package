"""Types for the storage facade."""

import typing

TKey = str
TPrefix = str
TSuffix = str
TKeys = typing.List[TKey]
TValue = str


class TStorage(typing.Protocol):
    """Interface for storage."""

    def list(
        self,
        prefix: typing.Optional[TPrefix] = None,
        suffix: typing.Optional[TSuffix] = None,
    ) -> TKeys:
        """
        List available objects.

        Args:
            prefix: The prefix any keys must match.
            suffix: The suffix any keys must match.

        Returns:
            All keys that match the prefix and suffix if they were supplied.

        """
        ...

    def get(self, *, key: TKey) -> TValue:
        """
        Get a seed by key.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object.

        Returns:
            The value of the object.

        """
        ...

    def set(self, *, key: TKey, value: TValue) -> None:
        """
        Set the object at a key to a value.

        Args:
            key: The key to the object.
            value: The value to set the object to.

        """
        ...

    def delete(self, *, key: TKey) -> None:
        """
        Delete an object by key.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object to delete.

        """
        ...

    def delete_all(self, *, keys: TKeys) -> None:
        """
        Delete the objects behind the keys.

        Args:
            keys: The keys of the objects to delete.

        """
        ...

"""Types for the storage facade."""

import typing

TKey = str
TPrefix = str
TPostfix = str
TKeys = typing.List[TKey]
TValue = str


class TStorage(typing.Protocol):
    """Interface for storage."""

    def list(self, prefix: typing.Optional[TPrefix] = None) -> TKeys:
        """List available objects."""
        ...

    def get(self, *, key: TKey) -> TValue:
        """Get an object by key."""
        ...

    def set(self, *, key: TKey, value: TValue) -> None:
        """Set a object key to a value."""
        ...

    def delete(self, *, key: TKey) -> None:
        """Delete an object key."""
        ...

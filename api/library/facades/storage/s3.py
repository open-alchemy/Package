"""S3 implementation for the storage facade."""

import typing

import boto3
from botocore import exceptions as botocore_exceptions

from . import exceptions, types


class Storage:
    """Interface for s3 storage."""

    def __init__(self, bucket: str) -> None:
        """Construct."""
        self.bucket = bucket
        self.client = boto3.client("s3")

    def _list_generator(self, prefix: str) -> typing.Generator[str, None, None]:
        """Create key generator."""
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            try:
                contents = page["Contents"]
            except KeyError:
                break

            for obj in contents:
                yield obj["Key"]

    def list(
        self,
        prefix: typing.Optional[types.TPrefix] = None,
        suffix: typing.Optional[types.TPrefix] = None,
    ) -> types.TKeys:
        """
        List available objects.

        Args:
            prefix: The prefix any keys must match.
            suffix: The suffix any keys must match.

        Returns:
            All keys that match the prefix if it was supplied.

        """
        try:
            prefix_keys = self._list_generator(
                prefix=prefix if prefix is not None else ""
            )
            prefix_suffix_keys = filter(
                lambda key: suffix is None or key.endswith(suffix), prefix_keys
            )
            return list(prefix_suffix_keys)
        except (
            botocore_exceptions.BotoCoreError,
            botocore_exceptions.ClientError,
        ) as exc:
            raise exceptions.StorageError from exc

    def get(self, *, key: types.TKey) -> types.TValue:
        """
        Get a seed by key.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object.

        Returns:
            The value of the object.

        """
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            return response["Body"].read().decode()
        except botocore_exceptions.BotoCoreError as exc:
            raise exceptions.StorageError(
                f"something went wrong when retriving key {key}"
            ) from exc
        except botocore_exceptions.ClientError as exc:
            raise exceptions.ObjectNotFoundError(
                f"could not find object at key {key}"
            ) from exc

    def set(self, *, key: types.TKey, value: types.TValue) -> None:
        """
        Set the object at a key to a value.

        Args:
            key: The key to the object.
            value: The value to set the object to.

        """
        try:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=value.encode())
        except (
            botocore_exceptions.BotoCoreError,
            botocore_exceptions.ClientError,
        ) as exc:
            raise exceptions.StorageError from exc

    def delete(self, *, key: types.TKey) -> None:
        """
        Delete an object by key.

        Raises ObjectNotFoundError if there is no object with that key.

        Args:
            key: The key of the object to delete.

        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
        except botocore_exceptions.BotoCoreError as exc:
            raise exceptions.StorageError(
                f"something went wrong when deleting key {key}"
            ) from exc
        except botocore_exceptions.ClientError as exc:
            raise exceptions.ObjectNotFoundError(
                f"could not find object at key {key}"
            ) from exc

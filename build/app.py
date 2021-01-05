"""Main function for lambda."""

import dataclasses
import json
import pathlib
import shutil
import typing
from urllib import parse

import boto3
import library
from botocore import client

S3_CLIENT = boto3.client("s3")


def setup(directory: str) -> pathlib.Path:
    """
    Prepare the environment for execution.

    Args:
        directory: The base directory for execution.

    Returns:
        The directory that can be used to execute.

    """
    path = pathlib.Path(directory)
    build_path = path / "build"
    if build_path.exists():
        if build_path.is_dir():
            shutil.rmtree(build_path)
        if build_path.is_file():
            build_path.unlink()

    assert not build_path.exists()
    build_path.mkdir()
    return build_path


@dataclasses.dataclass
class Notification:
    """
    The bucket and object key from the notification.

    bucket_name: The bucket from the notification.
    object_key: The object key from the notification.

    """

    bucket_name: str
    object_key: str


def parse_notification(notification: typing.Dict) -> Notification:
    """
    Parse a SNS notification.

    Args:
        notification: The information for the SNS notification.

    Returns:
        The bucket and object key from the notification.

    """
    records_key = "Records"
    assert records_key in notification, f"{records_key} not in message, {notification=}"
    records = notification[records_key]
    assert isinstance(records, list), (
        f"notification.{records_key} not list, " f"{records=}, {notification=}"
    )

    assert len(records) == 1, (
        f"notification.{records_key} does not have 1 item, "
        f"{records=}, {notification=}"
    )
    record = records[0]
    assert isinstance(record, dict), (
        f"notification.{records_key}[0] not dict, " f"{record=}, {notification=}"
    )

    s3_key = "s3"
    assert s3_key in record, (
        f"{s3_key} not in notification.{records_key}[0], " f"{record=}, {notification=}"
    )
    s3_value = record[s3_key]
    assert isinstance(s3_value, dict), (
        f"notification.{records_key}[0].{s3_key} is not a dict, "
        f"{s3_value=}, {notification=}"
    )

    s3_bucket_key = "bucket"
    assert s3_bucket_key in s3_value, (
        f"{s3_bucket_key} not in "
        f"notification.{records_key}[0].{s3_key}, "
        f"{s3_value=}, {notification=}"
    )
    s3_bucket = s3_value[s3_bucket_key]
    assert isinstance(s3_bucket, dict), (
        f"notification.{records_key}[0].{s3_key}.{s3_bucket_key} "
        "is not a dict, "
        f"{s3_bucket=}, {notification=}"
    )

    s3_bucket_name_key = "name"
    assert s3_bucket_name_key in s3_bucket, (
        f"{s3_bucket_name_key} not in "
        f"notification.{records_key}[0].{s3_key}.{s3_bucket_key}, "
        f"{s3_bucket=}, {notification=}"
    )
    s3_bucket_name = s3_bucket[s3_bucket_name_key]
    assert isinstance(s3_bucket_name, str), (
        f"notification.{records_key}[0].{s3_key}.{s3_bucket_key}"
        f".{s3_bucket_name_key} "
        "is not a string, "
        f"{s3_bucket_name=}, {notification=}"
    )

    s3_object_key = "object"
    assert s3_object_key in s3_value, (
        f"{s3_object_key} not in "
        f"notification.{records_key}[0].{s3_key}, "
        f"{s3_value=}, {notification=}"
    )
    s3_object = s3_value[s3_object_key]
    assert isinstance(s3_object, dict), (
        f"notification.{records_key}[0].{s3_key}.{s3_object_key} "
        "is not a dict, "
        f"{s3_object=}, {notification=}"
    )

    s3_object_key_key = "key"
    assert s3_object_key_key in s3_object, (
        f"{s3_object_key_key} not in "
        f"notification.{records_key}[0].{s3_key}.{s3_object_key}, "
        f"{s3_object=}, {notification=}"
    )
    s3_object_key = s3_object[s3_object_key_key]
    assert isinstance(s3_object_key, str), (
        f"notification.{records_key}[0].{s3_key}.{s3_object_key}"
        f".{s3_object_key_key} "
        "is not a string, "
        f"{s3_object_key=}, {notification=}"
    )

    return Notification(
        bucket_name=parse.unquote_plus(s3_bucket_name),
        object_key=parse.unquote_plus(s3_object_key),
    )


def parse_event(event: typing.Dict) -> Notification:
    """
    Parse a lambda event.

    Args:
        event: The information for the lambda event.

    Returns:
        The bucket and object key from the notification.

    """
    assert isinstance(event, dict), f"event not dict, {event=}"

    records_key = "Records"
    assert records_key in event, f"{records_key} not in event, {event=}"
    records = event[records_key]
    assert isinstance(
        records, list
    ), f"event.{records_key} not list, {records=}, {event=}"

    assert (
        len(records) == 1
    ), f"event.{records_key} does not have 1 item, {records=}, {event=}"
    record = records[0]
    assert isinstance(
        record, dict
    ), f"event.{records_key}[0] not dict, {record=}, {event=}"

    sns_key = "Sns"
    assert (
        sns_key in record
    ), f"{sns_key} not in event.{records_key}[0], {record=}, {event=}"
    sns = record[sns_key]
    assert isinstance(
        sns, dict
    ), f"event.{records_key}[0].{sns_key} is not a dict, {sns=}, {event=}"

    message_key = "Message"
    assert (
        message_key in sns
    ), f"{message_key} not in event.{records_key}[0].{sns_key}, {sns=}, {event=}"
    message = sns[message_key]
    assert isinstance(message, str), (
        f"event.{records_key}[0].{sns_key}.{message_key} is not a string, "
        f"{message=}, {event=}"
    )

    try:
        decoded_message = json.loads(message)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"event.{records_key}[0].{sns_key}.{message_key} is not a valid JSON, "
            f"{message=}, {event=}, {exc}"
        ) from exc
    assert isinstance(
        decoded_message, dict
    ), f"SNS message is not a dict, {decoded_message=}, {event=}"

    return parse_notification(decoded_message)


def retrieve_spec(notification: Notification, build_path: pathlib.Path) -> pathlib.Path:
    """
    Retrieve the spec from s3.

    Args:
        notification: The SNS notification with the bucket name and object key.
        build_path: The path where the build is done.

    Returns:
        The path to the spec file.

    """
    spec_path = build_path / "spec.json"
    S3_CLIENT.download_file(
        notification.bucket_name,
        notification.object_key,
        str(spec_path),
    )
    return spec_path


def upload_packages(notification: Notification, packages: library.PackageList) -> None:
    """
    Upload the packages to S3.

    Args:
        notification: The SNS notification.
        packages: The packages to upload.

    """
    for package in packages:
        S3_CLIENT.upload_file(
            str(package.path), notification.bucket_name, package.storage_location
        )


def spec_exists(notification: Notification) -> bool:
    """
    Check whether the spec exists.

    Args:
        notification: The SNS notification.

    Returns:
        Whether the spec file in the SNS notification exists.

    """
    response = S3_CLIENT.list_objects_v2(
        Bucket=notification.bucket_name, Prefix=notification.object_key
    )

    assert isinstance(response, dict), f"response is not dict, {response=}"

    key_count_key = "KeyCount"
    assert key_count_key in response, f"{key_count_key} not in response, {response=}"
    key_count = response[key_count_key]

    assert isinstance(
        key_count, int
    ), f"response.{key_count_key} is not int, {key_count=}, {response=}"

    return key_count == 1


def delete_packages_if_spec_deleted(
    spec_exists_result: bool, notification: Notification, packages: library.PackageList
) -> None:
    """
    Conditionally delete the packages if the spec has been deleted.

    Args:
        spec_exists_result: The result of the check whether the spec exists.
        notification: The SNS notification.
        packages: The packages to delete.

    """
    if spec_exists_result:
        return

    S3_CLIENT.delete_objects(
        Bucket=notification.bucket_name,
        Delete={"Objects": [{"Key": package.storage_location} for package in packages]},
    )


def main(event, _context):
    """Handle request."""
    build_path = setup("/tmp")
    notification = parse_event(event)
    try:
        spec_path = retrieve_spec(notification, build_path)
    except client.ClientError:
        return
    packages = library.generate(notification.object_key, spec_path)
    upload_packages(notification, packages)
    spec_exists_result = spec_exists(notification)
    delete_packages_if_spec_deleted(spec_exists_result, notification, packages)

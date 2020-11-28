"""tests for s3 torage facade."""

import pytest
from botocore import stub

from library.facades import storage


@pytest.mark.parametrize(
    "response, prefix, expected_prefix, expected_keys",
    [
        pytest.param({}, None, "", [], id="empty response"),
        pytest.param({}, "prefix 1", "prefix 1", [], id="empty response with prefix"),
        pytest.param(
            {"Contents": [{"Key": "key 1"}]},
            None,
            "",
            ["key 1"],
            id="single key response",
        ),
    ],
)
def test_list(response, prefix, expected_prefix, expected_keys):
    """
    GIVEN stubbed s3 client
    WHEN list is called
    THEN the keys are returned.
    """
    bucket = "bucket1"
    s3_instance = storage.s3.Storage(bucket)
    stubber = stub.Stubber(s3_instance.client)
    expected_params = {"Bucket": bucket, "Prefix": expected_prefix}
    stubber.add_response("list_objects_v2", response, expected_params)
    stubber.activate()

    returned_keys = s3_instance.list(prefix=prefix)

    stubber.assert_no_pending_responses()
    assert returned_keys == expected_keys


def test_list_multi_page():
    """
    GIVEN stubbed s3 client that has multiple pages
    WHEN list is called
    THEN the keys are returned.
    """
    bucket = "bucket1"
    key1 = "key 1"
    key2 = "key 2"
    s3_instance = storage.s3.Storage(bucket)
    stubber = stub.Stubber(s3_instance.client)
    continuation_token = "token 1"
    response1 = {
        "IsTruncated": True,
        "Contents": [
            {
                "Key": key1,
            }
        ],
        "NextContinuationToken": continuation_token,
    }
    expected_params1 = {"Bucket": bucket, "Prefix": ""}
    stubber.add_response("list_objects_v2", response1, expected_params1)
    response2 = {
        "Contents": [
            {
                "Key": key2,
            }
        ]
    }
    expected_params2 = {
        "Bucket": bucket,
        "Prefix": "",
        "ContinuationToken": continuation_token,
    }
    stubber.add_response("list_objects_v2", response2, expected_params2)
    stubber.activate()

    returned_keys = s3_instance.list()

    stubber.assert_no_pending_responses()
    assert returned_keys == [key1, key2]


def test_list_error_invalid_bucket():
    """
    GIVEN stubbed s3 client that raises an error
    WHEN list is called
    THEN StorageError is raised.
    """
    bucket = "bucket 1"
    s3_instance = storage.s3.Storage(bucket)
    stubber = stub.Stubber(s3_instance.client)
    stubber.activate()

    with pytest.raises(storage.exceptions.StorageError):
        s3_instance.list()

    stubber.assert_no_pending_responses()


def test_list_error_client():
    """
    GIVEN stubbed s3 client that raises an error
    WHEN list is called
    THEN StorageError is raised.
    """
    bucket = "bucket1"
    s3_instance = storage.s3.Storage(bucket)
    stubber = stub.Stubber(s3_instance.client)
    stubber.add_client_error("list_objects_v2")
    stubber.activate()

    with pytest.raises(storage.exceptions.StorageError):
        s3_instance.list()

    stubber.assert_no_pending_responses()

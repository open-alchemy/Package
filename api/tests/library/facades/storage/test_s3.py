"""tests for s3 torage facade."""

import pytest
from botocore import stub

from library.facades import storage


@pytest.mark.parametrize(
    "response, expected_keys", [({}, []), ({"Contents": [{"Key": "key 1"}]}, ["key 1"])]
)
def test_list(response, expected_keys):
    """
    GIVEN stubbed s3 client
    WHEN list is called
    THEN the keys are returned.
    """
    bucket = "bucket1"
    s3_instance = storage.s3.Storage(bucket)
    stubber = stub.Stubber(s3_instance.client)
    expected_params = {"Bucket": bucket, "Prefix": ""}
    stubber.add_response("list_objects_v2", response, expected_params)
    stubber.activate()

    returned_keys = s3_instance.list()

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

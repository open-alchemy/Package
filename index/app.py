"""Main function for lambda."""

# pylint: disable=wrong-import-position

import os

os.environ["STAGE"] = "PROD"

import dataclasses
import typing

import library
from library import types


@dataclasses.dataclass
class Request:
    """
    Key information from the event request.

    Attrs:
        authorization_value: The value of the Authorization header.
        uri: The requested uri.
    """

    authorization_value: str
    uri: str


@dataclasses.dataclass
class Event:
    """
    Key information from the event request.

    Attrs:
        authorization_value: The value of the Authorization header.
    """

    request: Request
    request_dict: typing.Dict


def parse_request(
    *, request: typing.Dict, event_prefix: str, event: typing.Dict
) -> Request:
    """
    Parse a lambda event request.

    Args:
        request: The information for the lambda event.
        event_prefix: The prefix for the request in the event.
        event: The information for the lambda event.

    Returns:
        Key information extracted from the event.

    """
    headers_key = "headers"
    assert (
        headers_key in request
    ), f"{headers_key} not in {event_prefix} {request=}, {event=}"
    headers = request[headers_key]
    assert isinstance(
        headers, dict
    ), f"{event_prefix}.{headers_key} is not a dictionary, {request=}, {event=}"

    authorization_key = "authorization"
    assert authorization_key in headers, (
        f"{authorization_key} not in {event_prefix}.{authorization_key}, "
        f"{headers=}, {event=}"
    )
    authorization = headers[authorization_key]
    assert isinstance(authorization, list), (
        f"{event_prefix}.{headers_key}.{authorization_key} is not a list, "
        f"{headers=}, {event=}"
    )

    assert len(authorization) == 1, (
        f"{event_prefix}.{headers_key}.{authorization_key} does not have 1 item, "
        f"{authorization=}, {event=}"
    )
    authorization_item = authorization[0]
    assert isinstance(authorization_item, dict), (
        f"{event_prefix}.{headers_key}.{authorization_key}[0] not dict, "
        f"{authorization_item=}, {event=}"
    )

    value_key = "value"
    assert value_key in authorization_item, (
        f"{value_key} not in {event_prefix}.{headers_key}.{authorization_key}[0] "
        f"{authorization_item=}, {event=}"
    )
    value = authorization_item[value_key]
    assert isinstance(value, str), (
        f"{event_prefix}.{headers_key}.{authorization_key}[0].{value_key} "
        "is not a string, "
        f"{value=}, {event=}"
    )

    uri_key = "uri"
    assert uri_key in request, (
        f"{uri_key} not in " f"{event_prefix}" f"{request=}, {event=}"
    )
    uri = request[uri_key]
    assert isinstance(uri, str), (
        f"{event_prefix}.{uri_key}" "is not a string, " f"{uri=}, {event=}"
    )

    return Request(authorization_value=value, uri=uri)


def parse_event(event: typing.Dict) -> Event:
    """
    Parse a lambda event.

    Args:
        event: The information for the lambda event.

    Returns:
        Key information extracted from the event.

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

    cf_key = "cf"
    assert (
        cf_key in record
    ), f"{cf_key} not in event.{records_key}[0], {record=}, {event=}"
    cf_value = record[cf_key]
    assert isinstance(
        cf_value, dict
    ), f"event.{records_key}[0].{cf_key} is not a dict, {cf_value=}, {event=}"

    request_key = "request"
    assert (
        request_key in cf_value
    ), f"{request_key} not in event.{records_key}[0].{cf_key}, {cf_value=}, {event=}"
    request = cf_value[request_key]
    assert isinstance(request, dict), (
        f"event.{records_key}[0].{cf_key}.{request_key} is not a dictionary, "
        f"{request=}, {event=}"
    )

    request_info = parse_request(
        request=request,
        event_prefix=f"event.{records_key}[0].{cf_key}.{request_key}",
        event=event,
    )

    return Event(request=request_info, request_dict=request)


def main(event, context):
    """Handle request."""
    print({"event": event, "context": context})  ## allow-print
    event_info = parse_event(event)
    print({"event_info": event_info})  ## allow-print
    response = library.process(
        uri=event_info.request.uri,
        authorization_value=event_info.request.authorization_value,
    )
    print({"response": response})  ## allow-print
    if response.type == types.TRequestType.LIST:
        return {
            "status": "200",
            "statusDescription": "OK",
            "headers": {
                "cache-control": [{"key": "Cache-Control", "value": "max-age=0"}],
                "content-type": [{"key": "Content-Type", "value": "text/html"}],
            },
            "body": response.value,
        }
    assert response.type == types.TRequestType.INSTALL
    request = event_info.request_dict
    request["uri"] = response.value
    return request

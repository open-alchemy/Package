"""Tests for the specs endpoint."""

from library import specs
from library.facades import storage


def test_put():
    """
    GIVEN body and spec id
    WHEN put is called with the body and spec id
    THEN the spec is stored against the spec id.
    """
    body = "body 1"
    spec_id = "id 1"

    specs.put(body=body, spec_id=spec_id)

    assert storage.get_storage().get(key=spec_id) == body

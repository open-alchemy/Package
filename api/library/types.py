"""Common types."""

import typing

TUser = str
TSpecName = str
TSpecId = str
TSpecValue = str
TSpecVersion = str
TSpecTitle = str
TSpecOptTitle = typing.Optional[TSpecTitle]
TSpecDescription = str
TSpecOptDescription = typing.Optional[TSpecDescription]
TSpecVersions = typing.List[TSpecVersion]
TSpecModelCount = int


class TResult(typing.NamedTuple):
    """
    The return value for a check.

    Attrs:
        value: The result of the check.
        reason: If the result is True, the reason that it is.

    """

    value: bool
    reason: typing.Optional[str]

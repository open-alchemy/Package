"""Common types."""

import typing

TUser = str
TSpecId = str
TSpecValue = str
TSpecVersion = str
TSpecTitle = str
TSpecOptTitle = typing.Optional[TSpecTitle]
TSpecDescription = str
TSpecOptDescription = typing.Optional[TSpecDescription]
TSpecVersions = typing.List[TSpecVersion]
TSpecModelCount = int

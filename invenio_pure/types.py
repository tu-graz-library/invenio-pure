# SPDX-FileCopyrightText: 2022-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Types of the pure connector."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import cast

type RequestsJsonType = (
    bool
    | str
    | int
    | float
    | list[RequestsJsonType]
    | dict[str, RequestsJsonType]
    | None
)

type JsonType = dict[str, RequestsJsonType]

URL = str
"""This type should be used wherever a URL is the value of the variable."""

PureToken = str
"""The Pure Token.

It will not have a special schema.
"""

PureRecord = dict
"""The record which will be imported from pure.

This record has to be a dict (json).
"""

FilePath = str
"""The path to the file on the local machine."""

EmailAddress = str
"""The email address.

The address does not have to have a special format, but it has to be an email.
"""

PureAPIKey = str
"""Pure api token."""

Filter = dict[str, list[str] | int]
"""The filter describes which records will be imported into the repository."""


@dataclass
class PureFile:
    """Pure File."""

    filename: str
    url: str

    def __init__(self, filename: str, url: str, **__: dict) -> None:
        """Construct."""
        self.filename = filename
        self.url = url

    @property
    def stem(self) -> str:
        """Stem property."""
        return Path(self.filename).stem

    @property
    def suffix(self) -> str:
        """Suffix property."""
        return Path(self.filename).suffix


@dataclass
class PureId:
    """Pure id."""

    uuid: str

    def __str__(self) -> str:
        """Stringify."""
        return self.uuid


@dataclass
class PureIds:
    """Pure Ids."""

    ids: list[PureId]

    def __init__(self, records: list[JsonType]) -> None:
        """Construct pure ids."""
        self.ids = [PureId(cast(str, record["uuid"])) for record in records]

    def __iter__(self) -> Iterator[PureId]:
        """Iterate."""
        return iter(self.ids)

# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""API."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

from ..types import Filter, JsonType, PureFile, PureId, PureIds
from .config import PureRESTConfig
from .models import PureConnection


class PureAPI:
    """Pure api."""

    connection_cls = PureConnection

    def __init__(self, config: PureRESTConfig) -> None:
        """Construct."""
        self.connection = self.connection_cls(config)

    def fetch_all_ids(self, filter_records: Filter) -> PureIds:
        """Get records."""
        return self.connection.ids(filter_records)

    def get_metadata(self, pure_id: PureId) -> JsonType:
        """Get metadata."""
        return self.connection.metadata(pure_id)

    def get_journal(self, journal_id: PureId) -> JsonType:
        """Get journal metadata."""
        return self.connection.journal(journal_id)

    def get_publisher(self, publisher_id: PureId) -> JsonType:
        """Get publisher metadata."""
        return self.connection.publisher(publisher_id)

    def get_publisher_name(self, pure_id: PureId) -> str:
        """Get publisher name."""
        metadata = cast(
            dict[str, dict[str, dict[str, str]]],
            self.get_metadata(pure_id),
        )

        try:
            journal_id = PureId(metadata["journalAssociation"]["journal"]["uuid"])
        except KeyError as error:
            msg = f"For pure_id: {pure_id} no journal was found."
            raise RuntimeError(msg) from error

        journal = cast(dict[str, dict[str, str]], self.get_journal(journal_id))

        try:
            publisher_id = PureId(journal["publisher"]["uuid"])
        except KeyError as error:
            msg = f"For pure_id: {pure_id} no publisher was found."
            raise RuntimeError(msg) from error

        publisher = cast(dict[str, str], self.get_publisher(publisher_id))

        try:
            name = publisher["name"]
        except KeyError as error:
            msg = f"For pure_id: {pure_id} no publisher name was found."
            raise RuntimeError(msg) from error

        return name

    def download_file(self, pure_file: PureFile) -> Path:
        """Download file."""
        prefix = pure_file.stem
        suffix = pure_file.suffix

        with NamedTemporaryFile(
            delete=False,
            delete_on_close=False,
            prefix=f"{prefix}-",
            suffix=suffix,
        ) as file_pointer:
            self.connection.store_file_temporarily(pure_file.url, file_pointer)
        return Path(file_pointer.name)

    def mark_as_exported(self, pure_id: PureId, record: JsonType) -> bool:
        """Mark as exported."""
        # this replaces dk/atira/pure/researchoutput/keywords/export2repo/validated
        record["keywordUris"] = [
            "dk/atira/pure/researchoutput/keywords/export2repo/exported",
        ]
        return self.connection.mark_as_exported(pure_id, record)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import SupportsIndex, cast

from ..types import JSON, Filter, PureID
from .config import PureRESTConfig
from .models import PureConnection


class PureAPI:
    """Pure api."""

    connection_cls = PureConnection

    def __init__(self, config: PureRESTConfig) -> None:
        """Construct."""
        self.connection = self.connection_cls(config)

    def fetch_all_ids(self, filter_records: Filter) -> list[str]:
        """Get records."""
        records = self.connection.ids(filter_records)
        return [record["uuid"] for record in records]

    def get_metadata(self, pure_id: PureID) -> dict[str, JSON]:
        """Get metadata."""
        return self.connection.metadata(pure_id)

    def get_journal(self, journal_id: PureID) -> JSON:
        """Get journal metadata."""
        return self.connection.journal(journal_id)

    def get_publisher(self, publisher_id: PureID) -> JSON:
        """Get publisher metadata."""
        return self.connection.publisher(publisher_id)

    def get_publisher_name(self, pure_id: PureID) -> str:
        """Get publisher name."""
        metadata = cast(
            dict[str, dict[str, dict[str, str]]],
            self.get_metadata(pure_id),
        )

        try:
            journal_id = metadata["journalAssociation"]["journal"]["uuid"]
        except KeyError as error:
            msg = f"For pure_id: {pure_id} no journal was found."
            raise RuntimeError(msg) from error

        journal = cast(dict[str, dict[str, str]], self.get_journal(journal_id))

        try:
            publisher_id = journal["publisher"]["uuid"]
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

    def download_file(self, file_: dict[str, str]) -> str:
        """Download file."""
        filename = file_["fileName"]
        prefix = Path(filename).stem
        suffix = Path(filename).suffix

        with NamedTemporaryFile(
            delete=False,
            delete_on_close=False,
            prefix=f"{prefix}-",
            suffix=suffix,
        ) as file_pointer:
            self.connection.store_file_temporarily(file_["url"], file_pointer)
        return file_pointer.name

    def mark_as_exported(self, pure_id: PureID, record: JSON) -> bool:
        """Mark as exported."""
        # TODO:
        # replace dk/atira/pure/researchoutput/keywords/export2repo/validated with
        # dk/atira/pure/researchoutput/keywords/export2repo/exported
        # not sure if the attribute worksl like that
        record[cast(SupportsIndex, "keywordUris")] = [
            "dk/atira/pure/researchoutput/keywords/export2repo/exported",
        ]
        return self.connection.mark_as_exported(pure_id, record)

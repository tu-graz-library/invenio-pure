# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API."""

from pathlib import Path

from ..types import URL, Filter, PureID
from .config import PureRESTConfig
from .models import PureConnection


class PureAPI:
    """Pure api."""

    connection_cls = PureConnection

    def __init__(self, config: PureRESTConfig) -> None:
        """Construct."""
        self.connection = self.connection_cls(config)

    def fetch_all_ids(self, filter_records: Filter) -> dict:
        """Get records."""
        records = self.connection.post_ids(filter_records)
        return [record.uuid for record in records]

    def get_metadata(self, pure_id: PureID) -> dict:
        """Get metadata."""
        return self.connection.post_metadata(pure_id)

    def download_file(self, pure_id: PureID, file_url: URL) -> Path:
        """Download file."""
        file_path = Path(f"/tmp/{pure_id}.pdf")  # noqa: S108
        self.store_file_temporarily(file_path, file_url)
        return file_path

    def mark_as_exported(self, pure_id: PureID, record: dict) -> bool:
        """Mark as exported."""
        # TODO:
        # replace dk/atira/pure/researchoutput/keywords/export2repo/validated with
        # dk/atira/pure/researchoutput/keywords/export2repo/exported
        # not sure if the attribute worksl like that
        record["keywordUris"] = [
            "dk/atira/pure/researchoutput/keywords/export2repo/exported",
        ]
        return self.connection.post_mark_as_exported(pure_id, record)

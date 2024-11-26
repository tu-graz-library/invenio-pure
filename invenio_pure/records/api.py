# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API."""

from pathlib import Path
from tempfile import NamedTemporaryFile

from ..types import Filter, PureID
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
        return [record["uuid"] for record in records["items"]]

    def get_metadata(self, pure_id: PureID) -> dict:
        """Get metadata."""
        return self.connection.metadata(pure_id)

    def download_file(self, file_: dict) -> str:
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

    def mark_as_exported(self, pure_id: PureID, record: dict) -> bool:
        """Mark as exported."""
        # TODO:
        # replace dk/atira/pure/researchoutput/keywords/export2repo/validated with
        # dk/atira/pure/researchoutput/keywords/export2repo/exported
        # not sure if the attribute worksl like that
        record["keywordUris"] = [
            "dk/atira/pure/researchoutput/keywords/export2repo/exported",
        ]
        return self.connection.mark_as_exported(pure_id, record)

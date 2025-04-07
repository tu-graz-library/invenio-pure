# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services."""


from flask_principal import Identity

from ..records import PureAPI
from ..types import JSON, Filter, PureID
from .config import PureRESTServiceConfig


class PureRESTService:
    """Pure rest service."""

    def __init__(self, config: PureRESTServiceConfig) -> None:
        """Construct."""
        self._config = config
        self.api = self.api_cls(config=config)

    @property
    def api_cls(self) -> type[PureAPI]:
        """Get api cls."""
        return self._config.api_cls

    def fetch_all_ids(self, _: Identity, filter_records: Filter) -> list[str]:
        """Fetch all ids from pure by given filter."""
        return self.api.fetch_all_ids(filter_records)

    def get_metadata(self, _: Identity, pure_id: PureID) -> dict[str, JSON]:
        """Get metadata by pure uuid."""
        return self.api.get_metadata(pure_id)

    def get_publisher_name(self, _: Identity, pure_id: PureID) -> str:
        """Get publisher information."""
        return self.api.get_publisher_name(pure_id)

    def download_file(self, _: Identity, file_: dict) -> str:
        """Download File."""
        return self.api.download_file(file_)

    def mark_as_exported(self, _: Identity, pure_id: PureID, record: dict) -> bool:
        """Mark as exported."""
        return self.api.mark_as_exported(pure_id, record)

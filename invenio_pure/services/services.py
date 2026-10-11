# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services."""

from pathlib import Path

from flask_principal import Identity

from ..records import PureAPI
from ..types import Filter, JsonType, PureFile, PureId, PureIds
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

    def fetch_all_ids(self, _: Identity, filter_records: Filter) -> PureIds:
        """Fetch all ids from pure by given filter."""
        return self.api.fetch_all_ids(filter_records)

    def get_metadata(self, _: Identity, pure_id: PureId) -> JsonType:
        """Get metadata by pure uuid."""
        return self.api.get_metadata(pure_id)

    def get_publisher_name(self, _: Identity, pure_id: PureId) -> str:
        """Get publisher information."""
        return self.api.get_publisher_name(pure_id)

    def download_file(self, _: Identity, pure_file: PureFile) -> Path:
        """Download File."""
        return self.api.download_file(pure_file)

    def mark_as_exported(
        self,
        _: Identity,
        pure_id: PureId,
        record: JsonType,
    ) -> bool:
        """Mark as exported."""
        return self.api.mark_as_exported(pure_id, record)

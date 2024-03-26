# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models."""


from pathlib import Path
from shutil import copyfileobj

from requests import ReadTimeout, get, post
from requests.auth import HTTPBasicAuth

from ..types import URL, Filter, PureAPIKey, PureID
from .config import PureRESTConfig


class PureRESTError(Exception):
    """Pure rest error."""

    def __init__(self, code: int, msg: str) -> None:
        """Create Pure rest error."""
        super().__init__(f"Pure REST error code={code} msg='{msg}'")


class PureRESTPOSTJson:
    """Pure rest post xml."""

    def __init__(self, api_key: PureAPIKey) -> None:
        """Construct."""
        self.api_key = api_key

    def create_request_headers(self) -> dict[str, str]:
        """Headers."""
        return {
            "api-key": self.api_key,
            "accept": "application/json",
            "Content-Type": "application/json",
        }


class PureConnection:
    """Pure connection."""

    def __init__(self, config: PureRESTConfig) -> None:
        """Construct."""
        self.config = config
        self.post_json = PureRESTPOSTJson(self.config.token)

    def post(self, endpoint: str, data: dict, headers: dict[str, str]) -> dict:
        """Post."""
        try:
            response = post(endpoint, data=data, headers=headers, timeout=10)
        except ReadTimeout as exc:
            raise PureRESTError(code=550, msg=str(exc)) from exc
        return response.json

    def post_ids(self, filter_records: Filter) -> list:
        """Post ids."""
        endpoint = f"{self.config.endpoint}/search"
        body = filter_records
        headers = self.post_json.create_request_headers()

        return self.post(endpoint, body, headers)

    def post_metadata(self, pure_id: PureID) -> dict:
        """Post metadata."""
        endpoint = f"{self.config.endpoint}/{pure_id}"
        body = {}
        headers = self.post_json.create_request_headers()

        return self.post(endpoint, body, headers)

    def store_file_temporarily(self, file_path: Path, file_url: URL) -> Path:
        """Download a file from Pure to given destination path with given file name.

        Return path to the downloaded file upon success, empty string upon failure.
        """
        auth = HTTPBasicAuth(self.config.username, self.config.password)

        with get(file_url, stream=True, auth=auth, timeout=10) as response:
            with file_path.open(mode="wb") as file_pointer:
                copyfileobj(response.raw, file_pointer)

        return file_path

    def post_mark_as_exported(self, pure_id: PureID, record: dict) -> bool:
        """Post mark as exported."""
        endpoint = f"{self.config.endpoint}/{pure_id}"
        body = record
        headers = self.post_json.create_request_headers()
        return self.post(endpoint, body, headers)

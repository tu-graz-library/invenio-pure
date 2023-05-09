# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Technische Universität Graz
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility methods."""
from http import HTTPStatus
from json import loads
from pathlib import Path
from shutil import copyfileobj

from requests import get
from requests.auth import HTTPBasicAuth

from .types import URL, FilePath, PureID


def headers(pure_api_key: str) -> dict[str, str]:
    """Headers."""
    return {
        "api-key": pure_api_key,
        "accept": "application/json",
    }


def get_research_output_count(pure_api_key: str, pure_api_url: str) -> int:
    """Get the amount of available research outputs at /research-outputs endpoint.

    Return -1 on failure.
    """
    url = f"{pure_api_url}/research-outputs"
    response = get(url, headers=headers(pure_api_key), timeout=10)

    if response.status_code != HTTPStatus.OK:
        return -1

    return int(loads(response.text)["count"])


def get_research_outputs(
    pure_api_key: str,
    pure_api_url: str,
    size: int,
    offset: int,
) -> list[dict]:
    """Get a list of research outputs.

    Pure API identifies a series by the following parameters:
    The *size* parameter defines the length of the series.
    The *offset* parameter defines the offset of the series.
    Return [] if the GET request is not OK.
    """
    url = f"{pure_api_url}/research-outputs?size={size}&offset={offset}"
    response = get(url, headers=headers(pure_api_key), timeout=10)

    if response.status_code != HTTPStatus.OK:
        return []

    response_json = loads(response.text)
    return response_json["items"]


def store_file_temporarily(
    file_url: URL,
    file_path: FilePath,
    auth: HTTPBasicAuth,
) -> None:
    """Download file."""
    with get(file_url, stream=True, auth=auth, timeout=10) as response:
        with Path(file_path).open(mode="wb") as file_pointer:
            copyfileobj(response.raw, file_pointer)


def download_file(
    pure_id: PureID,
    file_url: URL,
    pure_username: str,
    pure_password: str,
) -> str:
    """Download a file from Pure to given destination path with given file name.

    Return path to the downloaded file upon success, empty string upon failure.
    """
    file_path = f"/tmp/{pure_id}.pdf"  # noqa: S108
    auth = HTTPBasicAuth(pure_username, pure_password)
    store_file_temporarily(file_url, file_path, auth)

    return file_path

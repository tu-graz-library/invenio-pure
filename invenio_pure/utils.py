# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Technische Universität Graz
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility methods."""

from json import loads
from shutil import copyfileobj
from typing import Dict, List

from requests import get
from requests.auth import HTTPBasicAuth

from .types import URL, FilePath, PureID


def headers(pure_api_key: str) -> Dict[str, str]:
    headers = {
        "api-key": pure_api_key,
        "accept": "application/json",
    }
    return headers


def get_research_output_count(pure_api_key: str, pure_api_url: str) -> int:
    """Get the amount of available research outputs at /research-outputs endpoint.

    Return -1 on failure.
    """
    url = f"{pure_api_url}/research-outputs"
    response = get(url, headers=headers(pure_api_key))

    if response.status_code != 200:
        return -1

    return int(loads(response.text)["count"])


def get_research_outputs(
    pure_api_key: str, pure_api_url: str, size: int, offset: int
) -> List[dict]:
    """Get a list of research outputs.

    Pure API identifies a series by the following parameters:
    The *size* parameter defines the length of the series.
    The *offset* parameter defines the offset of the series.
    Return [] if the GET request is not OK.
    """
    url = f"{pure_api_url}/research-outputs?size={size}&offset={offset}"
    response = get(url, headers=headers(pure_api_key))

    if response.status_code != 200:
        return []

    response_json = loads(response.text)
    items = response_json["items"]
    return items


def store_file_temporarily(file_url: URL, file_path: FilePath, auth: HTTPBasicAuth):
    """Download file."""
    with get(file_url, stream=True) as response:
        with open(file_path, "wb") as fp:
            copyfileobj(response.raw, fp)


def download_pure_file(
    pure_id: PureID,
    file_url: URL,
    pure_username: str,
    pure_password: str,
) -> str:
    """Download a file from Pure to given destination path with given file name.

    Return path to the downloaded file upon success, empty string upon failure.
    """
    file_path = f"/tmp/{pure_id}.pdf"
    auth = HTTPBasicAuth(pure_username, pure_password)
    store_file_temporarily(file_url, file_path, auth)

    return file_path

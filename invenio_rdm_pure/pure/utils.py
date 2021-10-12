# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz
#
# invenio-rdm-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module containing requests for Pure."""

import json
from os.path import join
from typing import Dict, List

import requests
from requests.auth import HTTPBasicAuth


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
    response = requests.get(url, headers=headers(pure_api_key))

    if response.status_code != 200:
        return -1

    return int(json.loads(response.text)["count"])


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
    response = requests.get(url, headers=headers(pure_api_key))

    if response.status_code != 200:
        return []

    response_json = json.loads(response.text)
    items = response_json["items"]
    return items


def download_pure_file(
    file_url: str,
    pure_username: str,
    pure_password: str,
    destination_path: str,
    file_name: str,
) -> str:
    """Download a file from Pure to given destination path with given file name.

    Return path to the downloaded file upon success, empty string upon failure.
    """
    response = requests.get(file_url, auth=HTTPBasicAuth(pure_username, pure_password))
    if response.status_code != 200:
        return ""

    path = join(destination_path, file_name)
    with open(path, "wb") as fp:
        fp.write(response.content)

    return path

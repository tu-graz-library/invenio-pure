# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Technische Universität Graz
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Click options."""

from json import JSONDecodeError, loads
from pathlib import Path
from typing import Any

from click import ParamType, secho


def load_file_as_string(path: str) -> str:
    """Open a file and return the content as UTF-8 encoded string."""
    if not Path(path).is_absolute(path):
        path = Path(__file__).parent / path

    if not Path(path).is_file():
        return ""

    with Path(path).open(mode="rb") as file_pointer:
        content = file_pointer.read()
        return content.decode("utf-8")


class JSON(ParamType):
    """JSON provides the ability to load a json from a string or a file."""

    name = "JSON"

    def convert(
        self,
        value: Any,  # noqa: ANN401
        param: Any,  # noqa: ANN401, ARG002
        ctx: Any,  # noqa: ANN401, ARG002
    ) -> str:
        """Convert the json-str or json-file to the dictionary representation."""
        if Path(value).is_file():
            value = load_file_as_string(value)

        try:
            return loads(value)
        except JSONDecodeError:
            secho("ERROR - Invalid JSON provided.", fg="red")

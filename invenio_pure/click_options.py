# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Technische Universität Graz
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Click options."""

from json import JSONDecodeError, loads
from os.path import dirname, isabs, isfile, join

from click import ParamType, secho


def load_file_as_string(path):
    """Open a file and return the content as UTF-8 encoded string."""
    if not isabs(path):
        path = join(dirname(__file__), path)

    if not isfile(path):
        return ""

    with open(path, "rb") as fp:
        content = fp.read()
        return content.decode("utf-8")


class JSON(ParamType):
    """JSON provides the ability to load a json from a string or a file."""

    name = "JSON"

    def convert(self, value, param, ctx):
        """This method converts the json-str or json-file to the dictionary representation."""
        if isfile(value):
            value = load_file_as_string(value)

        try:
            return loads(value)
        except JSONDecodeError:
            secho("ERROR - Invalid JSON provided.", fg="red")

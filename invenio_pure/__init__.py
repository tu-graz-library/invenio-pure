# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""

from .errors import PureAPIError, PureRuntimeError
from .ext import InvenioPure
from .types import URL, PureID

__version__ = "1.3.0"

__all__ = (
    "__version__",
    "InvenioPure",
    "PureID",
    "PureAPIError",
    "PureRuntimeError",
    "URL",
)

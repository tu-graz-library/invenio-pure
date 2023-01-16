# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""

from .errors import PureAPIError, PureRuntimeError
from .ext import InvenioPure
from .types import URL, PureConfigs, PureID, PureRecord

__version__ = "0.1.2"

__all__ = (
    "__version__",
    "InvenioPure",
    "PureConfigs",
    "PureRecord",
    "PureID",
    "PureAPIError",
    "PureRuntimeError",
    "URL",
)

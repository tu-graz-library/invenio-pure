# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module that adds pure."""

from .errors import PureAPIError, PureRuntimeError
from .ext import InvenioPure
from .types import URL, PureID

__version__ = "1.4.0"

__all__ = (
    "__version__",
    "InvenioPure",
    "PureID",
    "PureAPIError",
    "PureRuntimeError",
    "URL",
)

# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Helper proxy to the state object."""

from typing import cast

from flask import current_app
from werkzeug.local import LocalProxy

from .ext import InvenioPure

current_pure: InvenioPure = cast(
    InvenioPure,
    LocalProxy(
        lambda: current_app.extensions["invenio-pure"],
    ),
)
"""Helper proxy to get teh current pure extension."""

# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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

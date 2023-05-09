# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Technische Universität Graz.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""

from flask import Flask


class InvenioPure:
    """invenio-pure extension."""

    def __init__(self, app: Flask = None) -> None:
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        app.extensions["invenio-pure"] = self

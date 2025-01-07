# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""

from flask import Flask

from .services import PureRESTService, PureRESTServiceConfig


class InvenioPure:
    """invenio-pure extension."""

    def __init__(self, app: Flask | None = None) -> None:
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_services(app)
        app.extensions["invenio-pure"] = self

    def init_services(self, app: Flask) -> None:
        """Initialize services."""
        endpoint = app.config.get("PURE_ENDPOINT", "")
        token = app.config.get("PURE_TOKEN", "")
        config = PureRESTServiceConfig(endpoint, token)
        self.pure_rest_service = PureRESTService(config)

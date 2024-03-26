# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 Technische Universität Graz.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask

from invenio_pure import InvenioPure, __version__


def test_version() -> None:
    """Test version import."""
    assert __version__


def test_init() -> None:
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioPure(app)
    assert "invenio-pure" in app.extensions

    app = Flask("testapp")
    ext = InvenioPure()
    assert "invenio-pure" not in app.extensions
    ext.init_app(app)
    assert "invenio-pure" in app.extensions

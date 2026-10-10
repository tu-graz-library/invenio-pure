# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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

# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

from collections.abc import Callable

import pytest
from flask import Flask

from invenio_pure import InvenioPure


@pytest.fixture(scope="module")
def create_app[**P](instance_path: str) -> Callable[P, Flask]:
    """Application factory fixture."""

    def factory(*_: P.args, **kwargs: P.kwargs) -> Flask:
        app = Flask("testapp", instance_path=instance_path)
        app.config.update(**kwargs)
        InvenioPure(app)
        return app

    return factory

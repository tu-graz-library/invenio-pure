# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 Technische Universität Graz.
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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

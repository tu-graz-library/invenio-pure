# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Technische Universität Graz.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
import os
import shutil
import tempfile

import pytest

# from flask import Flask
# from flask_babelex import Babel
# from invenio_access import InvenioAccess
# from invenio_accounts import InvenioAccounts
# from invenio_config import InvenioConfigDefault
# from invenio_db import InvenioDB, db

# from invenio_rdm_pure import InvenioRdmPure
# from invenio_rdm_pure.views import blueprint


# @pytest.fixture(scope="module")
# def celery_config():
#     """Override pytest-invenio fixture.

#     TODO: Remove this fixture if you add Celery support.
#     """
#     return {}


# @pytest.fixture(scope="module")
# def create_app(instance_path):
#     """Application factory fixture."""

#     def factory(**config):
#         app = Flask("testapp", instance_path=instance_path)
#         app.config.update(**config)
#         Babel(app)
#         InvenioRdmPure(app)
#         app.register_blueprint(blueprint)
#         return app

#     return factory


# @pytest.fixture()
# def base_app(request):
#     """Basic Flask application."""
#     instance_path = tempfile.mkdtemp()
#     app = Flask("testapp")

#     app.config.update(
#         SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://"),
#         SQLALCHEMY_TRACK_MODIFICATIONS=False,
#         TESTING=True,
#         SECRET_KEY="testing",
#     )

#     InvenioConfigDefault(app)
#     InvenioDB(app)
#     InvenioAccounts(app)
#     InvenioAccess(app)
#     InvenioRdmPure(app)

#     with app.app_context():
#         db_url = str(db.engine.url)
#         if db_url != "sqlite://" and not database_exists(db_url):
#             create_database(db_url)
#         db.create_all()

#     def teardown():
#         with app.app_context():
#             db_url = str(db.engine.url)
#             db.session.close()
#             if db_url != "sqlite://":
#                 drop_database(db_url)
#             shutil.rmtree(instance_path)

#     request.addfinalizer(teardown)
#     app.test_request_context().push()

#     return app

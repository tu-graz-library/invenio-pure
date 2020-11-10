# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Technische Universität Graz
#
# invenio-rdm-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""File description."""

import os

# import psycopg2
# import yaml
from flask import current_app
from flask_security.utils import hash_password
from invenio_db import db

from ...setup import database_uri, dirpath
from ..reports import Reports


class RdmDatabase:
    """Responsible for database connection and querying."""

    def __init__(self):
        """Description."""
        self.report = Reports()
        self._db_connect()

    # def _db_connect(self):
    #     """Establis a connection to RDM database."""
    #     host = current_app.config.get("INVENIO_DATABASE_HOST")
    #     name = current_app.config.get("INVENIO_DATABASE_NAME")
    #     user = current_app.config.get("INVENIO_DATABASE_USERNAME")
    #     password = current_app.config.get("INVENIO_DATABASE_PASSWORD")

    #     connection = psycopg2.connect(
    #         f"""\
    #         host={host} \
    #         dbname={name} \
    #         user={user} \
    #         password={password} \
    #         """
    #     )
    #     self.cursor = connection.cursor()

    def select_query(self, fields: str, table: str, filters={}):
        """Makes a select query to the database."""
        # Creating filters string
        filters_str = ""
        if filters:
            filters_str += " WHERE"
            for key in filters:
                filters_str += f" {key} = {filters[key]} AND"
            filters_str = filters_str[:-4]
        # Query
        query = f"SELECT {fields} FROM {table}{filters_str};"

        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        return self.cursor.fetchall()

    def get_pure_user_id(self):
        """Gets the userId of the Pure user.

        In case the user doesn't exist yet,
        it is created with credentials defined in config.py.
        """
        datastore = current_app.extensions["security"].datastore
        if datastore is not None:
            invenio_pure_user_email = current_app.config.get("INVENIO_PURE_USER_EMAIL")
            invenio_pure_user_password = current_app.config.get(
                "INVENIO_PURE_USER_PASSWORD"
            )
            invenio_pure_user = datastore.get_user(invenio_pure_user_email)
            if not invenio_pure_user:
                invenio_pure_user = datastore.create_user(
                    email=invenio_pure_user_email,
                    password=hash_password(invenio_pure_user_password),
                    active=True,
                )
                db.session.commit()
            return invenio_pure_user.id

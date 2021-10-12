# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz
#
# invenio-rdm-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility methods."""

import functools
import json
import smtplib
from datetime import datetime
from os.path import dirname, isabs, isfile, join
from typing import List

import click
from flask import current_app
from flask.cli import with_appcontext

# from flask_security.utils import hash_password

# from invenio_db import db


class JSON(click.ParamType):
    """JSON provides the ability to load a json from a string or a file."""

    name = "JSON"

    def convert(self, value, param, ctx):
        """This method converts the json-str or json-file to the dictionary representation."""
        if isfile(value):
            value = load_file_as_string(value)

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            click.secho("ERROR - Invalid JSON provided.", fg="red")


def get_user_id(user_email: str, user_password: str):
    """Get the userId of the user.

    In case the user doesn't exist yet,
    create it with given credentials.

    if the user does not exist it should be created with:


       user = datastore.create_user(
           email=user_email,
           password=hash_password(user_password),
           active=True,
       )
       db.session.commit()

    """
    datastore = current_app.extensions["security"].datastore
    user_id = ""  # not knowing the type, so it is "", maybe its a int
    if datastore is not None:
        user = datastore.get_user(user_email)
        if user:
            user_id = user.id

    return user_id


def make_user_admin(self, id_or_email: str) -> None:
    """Gives the user with given id or email administrator rights."""
    return None  # FIXME: Method stub'd until auxiliary methods are implemented.
    datastore = current_app.extensions["security"].datastore
    if datastore is not None:
        invenio_pure_user = datastore.get_user(
            id_or_email
        )  # FIXME: Not implemented yet.
        admin_role = datastore.find_role("admin")  # FIXME: Not implemented yet.
        datastore.add_role_to_user(invenio_pure_user, admin_role)


def load_file_as_string(path):
    """Open a file and return the content as UTF-8 encoded string."""
    if not isabs(path):
        path = join(dirname(__file__), path)

    if not isfile(path):
        return ""

    with open(path, "rb") as fp:
        input = fp.read()
        return input.decode("utf-8")


def get_dates_in_span(
    start: datetime.date, stop: datetime.date, step: int
) -> List[datetime.date]:
    """Returns an ascending list of dates with given step between the two endpoints of the span."""
    dates = []
    if start == stop:
        return [start]
    elif step == 0:
        return []
    elif step < 0:
        if start < stop:
            return []
        else:
            while start >= stop:
                dates.append(start)
                start += datetime.timedelta(step)
            dates.reverse()
    elif step > 0:
        if stop < start:
            return []
        else:
            while start <= stop:
                dates.append(start)
                start += datetime.timedelta(step)
    return dates


def send_email(
    uuid: str,
    file_name: str,
    email_sender: str,
    email_sender_password: str,
    email_receiver: str,
):
    """Send an email."""
    email_smtp_server = "smtp.gmail.com"
    email_smtp_port = 587
    email_subject = "Delete Pure File"
    email_message = (
        """Subject: """
        + email_subject
        + """Please remove from pure uuid {} the file {}."""
    )
    # create SMTP session
    session = smtplib.SMTP(email_smtp_server, email_smtp_port)

    # start TLS for security
    session.starttls()

    # Authentication
    session.login(email_sender, email_sender_password)

    # sending the mail
    message = email_message.format(uuid, file_name)
    session.sendmail(email_sender, email_receiver, message)

    # terminating the session
    session.quit()


@with_appcontext
def pure_user_id(func):
    """Decorator to give the pure_user_id to a function/method."""
    pure_user_email = current_app.config.get("PURE_USER_EMAIL")
    pure_user_password = current_app.config.get("PURE_USER_PASSWORD")

    pure_user_id = get_user_id(pure_user_email, pure_user_password)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs["pure_user_id"] = pure_user_id
        return func(*args, **kwargs)

    return wrapper

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Technische Universität Graz
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Scheduled tasks for celery."""

from collections.abc import Callable

from celery import shared_task
from flask import current_app
from flask_mail import Message

from .api import import_from_pure, pure_records
from .types import PureConfigs


def config_variables() -> tuple[Callable, Callable, PureConfigs]:
    """Collect variables."""
    import_func = current_app.config["PURE_IMPORT_FUNC"]
    sieve_func = current_app.config["PURE_SIEVE_FUNC"]
    endpoint = current_app.config["PURE_PURE_ENDPOINT"]
    token = current_app.config["PURE_PURE_TOKEN"]
    pure_username = current_app.config["PURE_PURE_USERNAME"]
    pure_password = current_app.config["PURE_PURE_PASSWORD"]
    user_email = current_app.config["PURE_USER_EMAIL"]
    recipients = current_app.config["PURE_ERROR_MAIL_RECIPIENTS"]
    sender = current_app.config["PURE_ERROR_MAIL_SENDER"]

    pure_configs = PureConfigs(
        endpoint,
        token,
        pure_username,
        pure_password,
        user_email,
        recipients,
        sender,
    )

    return import_func, sieve_func, pure_configs


@shared_task(ignore_result=True)
def import_records_from_pure() -> None:
    """Import records from pure."""
    import_func, sieve_func, configs = config_variables()

    for pure_record in pure_records(configs):
        if not sieve_func(pure_record):
            continue

        try:
            import_from_pure(import_func, pure_record, configs)
        except RuntimeError:
            msg = Message(
                "ERROR: importing from pure",
                sender=configs.sender,
                recipients=configs.recipients,
                body="record id",
            )
            current_app.extensions["mail"].send(msg)

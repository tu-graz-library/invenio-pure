# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands for Invenio-RDM-Pure."""


from click import STRING, group, option, secho
from click_params import URL
from flask import current_app
from flask.cli import with_appcontext

from .api import import_from_pure
from .click_options import JSON
from .types import PureConfigs


@group()
def pure() -> None:
    """Commands for InvenioRdmPure."""


@pure.command("import")
@with_appcontext
@option("--endpoint", type=URL)
@option("--token", type=STRING)
@option("--pure_username", type=STRING)
@option("--pure_password", type=STRING)
@option("--user-email", type=STRING)
@option("--pure-record", type=JSON())
@option("--no-color", is_flag=True, default=False)
def import_records_from_pure(
    endpoint: str,
    token: str,
    pure_username: str,
    pure_password: str,
    user_email: str,
    pure_record: dict,
    *,
    no_color: bool,
) -> None:
    """Import a record from given JSON file or JSON string."""
    import_func = current_app.config["PURE_IMPORT_FUNC"]
    recipients = current_app.config["PURE_ERROR_MAIL_RECIPIENTS"]
    sender = current_app.config["PURE_ERROR_MAIL_SENDER"]
    configs = PureConfigs(
        endpoint,
        token,
        pure_username,
        pure_password,
        user_email,
        recipients,
        sender,
    )
    record = import_from_pure(import_func, pure_record, configs)
    color = "green" if not no_color else "black"
    secho(f"record.id: {record.id}", fg=color)

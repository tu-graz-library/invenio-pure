# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands for Invenio-RDM-Pure."""


from click import STRING, group, option, secho
from click_params import URL
from flask import current_app
from flask.cli import with_appcontext
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts

from .services import PureRESTService, build_service


@group()
def pure() -> None:
    """Commands for InvenioRdmPure."""


@pure.command("import")
@with_appcontext
@option("--endpoint", type=URL, required=True)
@option("--token", type=STRING, required=True)
@option("--username", type=STRING, required=True)
@option("--password", type=STRING, required=True)
@option("--user-email", type=STRING, required=True)
@option("--pure-id", type=STRING, required=True)
@option("--no-color", is_flag=True, default=False)
@build_service
def import_records_from_pure(
    pure_service: PureRESTService,
    user_email: str,
    pure_id: str,
    *,
    no_color: bool,
) -> None:
    """Import a record from given JSON file or JSON string."""
    import_func = current_app.config["PURE_IMPORT_FUNC"]
    user = current_accounts.datastore.get_user_by_email(user_email)
    identity = get_identity(user)
    record = import_func(identity, pure_id, pure_service)

    color = "green" if not no_color else "black"
    secho(f"record.id: {record.id}", fg=color)

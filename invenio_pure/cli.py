# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands for Invenio-RDM-Pure."""


from collections.abc import Callable
from functools import wraps
from typing import Concatenate

from click import STRING, group, option, secho
from click_params import URL
from flask import current_app
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts

from .services import PureRESTService, build_service


def build_identity[**P, T](
    func: Callable[P, T],
) -> Callable[Concatenate[Identity, P], T]:
    """Decorate to build the user."""

    @wraps(func)
    def build(*args: P.args, **kwargs: P.kwargs) -> T:
        user = current_accounts.datastore.get_user_by_email(kwargs["user_email"])
        identity = get_identity(user)
        identity.provides.add(any_user)
        kwargs["identity"] = identity
        del kwargs["user_email"]

        return func(*args, **kwargs)

    return build


@group()
def pure() -> None:
    """Commands for InvenioRdmPure."""


@pure.command("import")
@with_appcontext
@option("--endpoint", type=URL, required=True)
@option("--token", type=STRING, required=True)
@option("--user-email", type=STRING, required=True)
@option("--pure-id", type=STRING, required=True)
@option("--no-color", is_flag=True, default=False)
@build_service
@build_identity
def import_records_from_pure(
    pure_service: PureRESTService,
    identity: Identity,
    pure_id: str,
    *,
    no_color: bool,
) -> None:
    """Import a record from given JSON file or JSON string."""
    import_func = current_app.config["PURE_IMPORT_FUNC"]

    try:
        record = import_func(identity, pure_id, pure_service)
        color = "green" if not no_color else "black"
        secho(f"record.id: {record.id}", fg=color)
    except RuntimeError as e:
        msg = f"ERROR pure pure_id: {pure_id} with message: {e!r}"
        color = "red" if not no_color else "black"
        secho(msg, fg=color)


@pure.command("list")
@with_appcontext
@option("--endpoint", type=URL, required=True)
@option("--token", type=STRING, required=True)
@option("--user-email", type=STRING, required=True)
@build_service
@build_identity
def list_all_available_records(
    pure_service: PureRESTService,
    identity: Identity,
) -> None:
    """List all possible to import records."""
    filter_records = current_app.config["PURE_FILTER_RECORDS"]

    for pure_id in pure_service.fetch_all_ids(identity, filter_records):
        secho(f"pure_id: {pure_id}", fg="green")


@pure.command("sync")
@with_appcontext
@option("--endpoint", type=URL, required=True)
@option("--token", type=STRING, required=True)
@option("--user-email", type=STRING, required=True)
@build_service
@build_identity
def sync(pure_service: PureRESTService, identity: Identity) -> None:
    """Sync Pure with the repo."""
    import_func = current_app.config["PURE_IMPORT_FUNC"]
    filter_records = current_app.config["PURE_FILTER_RECORDS"]

    ids = pure_service.fetch_all_ids(identity, filter_records)

    for pure_id in ids:
        try:
            import_func(identity, pure_id, pure_service)
            msg = f"SUCCESS pure pure_id: {pure_id} imported successfully."
            secho(msg, fg="green")
        except RuntimeError as e:
            msg = f"ERROR pure pure_id: {pure_id} with message: {e!r}"
            secho(msg, fg="red")

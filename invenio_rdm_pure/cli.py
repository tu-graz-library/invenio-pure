# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands for Invenio-RDM-Pure."""


import click
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access.permissions import any_user
from invenio_records_marc21 import current_records_marc21
from invenio_records_marc21.cli import fake_access_right, fake_feature_date
from invenio_records_marc21.services import Marc21Metadata

from .converter import Pure2Marc21
from .fixtures import create_demo_record
from .utils import JSON, pure_user_id


@pure_user_id
def create_marc21_record(pure_record: dict, pure_user_id: int) -> None:
    """Create a record."""
    converter = Pure2Marc21()
    marc21_record = Marc21Metadata()
    converter.convert(pure_record, marc21_record)

    identity = Identity(pure_user_id)
    identity.provides.add(any_user)

    fake_access = {
        "access_right": fake_access_right(),
        "embargo_date": fake_feature_date(),
    }

    service = current_records_marc21.records_service
    draft = service.create(
        identity=identity, metadata=marc21_record, access=fake_access
    )
    record = service.publish(id_=draft.id, identity=identity)
    click.secho(f"Record ({record.id}) converted and stored successfully.", fg="green")


@click.group()
def pure():
    """Commands for InvenioRdmPure."""
    pass


@pure.command("import")
@click.option("--data", type=JSON())
@with_appcontext
def import_json(data):
    """Import a record from given JSON file or JSON string."""
    create_marc21_record(data)


@pure.command()
@click.option(
    "--number",
    "-n",
    default=10,
    show_default=True,
    type=int,
    help="Number of demo records to be converted and stored.",
)
@with_appcontext
def demo(number):
    """Demonstrate conversion and storage of Pure records."""
    click.echo("Creating demo records...")

    for _ in range(number):
        demo_record = create_demo_record()
        create_marc21_record(demo_record)

    click.secho("Demo records created succesfully.", fg="green")

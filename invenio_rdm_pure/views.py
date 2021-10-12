# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz.
#
# invenio-rdm-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""

from flask import Blueprint

blueprint = Blueprint(
    "invenio_rdm_pure",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@blueprint.route("/export/<target_system>")
def export(target_system):
    """Render pure_import_xml view."""
    if target_system == "pure":
        pure_import_file = join(dirname(abspath(__file__)), "data", "TODO path to file")
        return open(pure_import_file, "r").read()

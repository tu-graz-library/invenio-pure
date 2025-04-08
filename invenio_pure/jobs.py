# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Jobs for Invenio-RDM-Pure."""

from invenio_jobs.jobs import JobType

from .tasks import import_records_from_pure


class PureImportJob(JobType):
    """Pure import job."""

    id = "pure_import_job"
    title = "Import Pure Records."
    description = "Import record from pure"

    task = import_records_from_pure

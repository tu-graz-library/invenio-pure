# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Jobs for Invenio-RDM-Pure."""

from invenio_jobs.jobs import JobType

from .tasks import (
    import_records_from_pure,
    list_all_available_records,
    mark_as_exported_in_pure,
)


class PureImportJob(JobType):
    """Pure import job."""

    id = "pure_import_job"
    title = "Import Pure Records."
    description = "Import record from pure"

    task = import_records_from_pure


class PureMarkAsExported(JobType):
    """Pure mark as exported job."""

    id = "pure_mark_as_exported_job"
    title = "Mark as exported in Pure."
    description = "Mark records in Pure with the tag mark-as-exported"

    task = mark_as_exported_in_pure


class ListAllAvailableRecords(JobType):
    """List all available records."""

    id = "list_all_available_records"
    title = "List all available records."
    description = "List all records which are ready imported."

    task = list_all_available_records

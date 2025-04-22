# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Scheduled tasks for celery."""


from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity

from .proxies import current_pure


@shared_task(ignore_result=True)
def import_records_from_pure() -> None:
    """Import records from pure."""
    current_app.logger.info("start import records from pure.")
    import_func = current_app.config["PURE_IMPORT_FUNC"]
    filter_records = current_app.config["PURE_FILTER_RECORDS"]

    pure_service = current_pure.pure_rest_service
    ids = pure_service.fetch_all_ids(system_identity, filter_records)

    for pure_id in ids:
        try:
            import_func(system_identity, pure_id, pure_service)
            msg = "SUCCESS pure pure_id: %s"
            current_app.logger.info(msg, pure_id)
        except RuntimeError as e:
            msg = "ERROR pure pure_id: %s with message: %s"
            current_app.logger.error(msg, pure_id, str(e))

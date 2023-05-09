# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Technische Universität Graz.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""
from collections.abc import Callable

from .types import (
    URL,
    EmailAddress,
    FilePath,
    PureConfigs,
    PureID,
    PurePassword,
    PureRecord,
    PureToken,
    PureUsername,
)

PURE_CELERY_BEAT_SCHEDULE = {}
"""The celery beat schedule is used to configure the import schedule.

Following is a example configuration. One option to add this to the
global celery beat schedule is to update the CELERY_BEAT_SCHEDULE
dict in invenio.cfg by the example below:

.. code-block:: python

    "synchronize_records": {
        "task": "invenio_pure.tasks.import_records_from_pure",
        "schedule": crontab(hour=1, minute=0, day_of_week=0),
    }
"""

PURE_IMPORT_FUNC: Callable[
    [
        PureRecord,
        PureConfigs,
        Callable[[PureID, URL, PureUsername, PurePassword], FilePath],
    ],
    None,
] = None
"""This function is called to import the pure record into the repository.

It needs as an parameter the pure record as a json, the pure configuration
and a callable which is provided from this package to download the file
from pure."""

PURE_SIEVE_FUNC: Callable[[PureRecord], bool] = None
"""This function implements the import criteria.

The import criteria handles the conditions which have to be true
as that the record will be imported into the repository.
"""

PURE_PURE_ENDPOINT: URL = ""
"""This is the endpoint of the pure instance."""

PURE_PURE_TOKEN: PureToken = ""
"""This is the token to be allowed to use the API."""

PURE_PURE_USERNAME: PureUsername = ""
"""This is the pure username which is necessary to download files."""

PURE_PURE_PASSWORD: PurePassword = ""
"""This is the pure password which is necessary to download files."""

PURE_USER_EMAIL: EmailAddress = ""
"""This is the user email of the pure user within the InvenioRDM instance."""

PURE_ERROR_MAIL_RECIPIENTS: list[EmailAddress] = []
"""The list of recipients to send emails if errors happen in the import process."""

PURE_ERROR_MAIL_SENDER: EmailAddress = ""
"""The sender of the error emails."""

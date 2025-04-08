# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure.

The celery beat schedule is used to configure the import schedule.

Following is a example configuration. One option to add this to the
global celery beat schedule is to update the CELERY_BEAT_SCHEDULE
dict in invenio.cfg by the example below:

.. code-block:: python

    "synchronize_records": {
        "task": "invenio_pure.tasks.import_records_from_pure",
        "schedule": crontab(hour=1, minute=0, day_of_week=0),
    }
"""


from .types import URL, EmailAddress, PureToken

PURE_ENDPOINT: URL = ""
"""This is the endpoint of the pure instance."""

PURE_TOKEN: PureToken = ""
"""This is the token to be allowed to use the API."""

PURE_USER_EMAIL: EmailAddress = ""
"""This is the user email of the pure user within the InvenioRDM instance."""

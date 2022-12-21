# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds pure."""

PURE_CELERY_BEAT_SCHEDULE = {}
"""Celery example sync configuration
example:
    "synchronize_records": {
        "task": "invenio_pure.tasks.synchronize_records",
        "schedule": crontab(hour=1, minute=0, day_of_week=0),
    }
"""

# # Invenio
# PURE_HOST_URL = "https://127.0.0.1:5000/"
# """URL of invenio host."""

# PURE_RECORD_URL = INVENIO_PURE_HOST_URL + "api/records/{}"
# """Endpoint to access single a record."""

# PURE_RECORDS_URL = INVENIO_PURE_HOST_URL + "api/records"
# """Endpoint to access multiple records."""

# PURE_USER_EMAIL = ""
# """Email of user creating the records."""

# PURE_USER_PASSWORD = ""
# """Password of user creating the records."""


# Pure
PURE_API_URL = ""
"""URL of the Pure Instance's REST API."""

PURE_API_KEY = ""
"""Token/Key of the Pure Instance's REST API."""

PURE_USERNAME = ""
"""Username of Pure user having the necessary permissions to acquire needed Pure entries."""

PURE_PASSWORD = ""
"""Password of Pure user having the necessary permissions to acquire needed Pure entries."""

PURE_RESPONSIBLE_EMAIL = ""
"""Email address of Pure user having the necessary permissions to delete Pure entries."""

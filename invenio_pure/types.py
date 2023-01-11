# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Types of the pure connector."""
from dataclasses import dataclass

PureID = str
"""This describes the main id used in pure.

This is the reference between the invenioRDM instance and the PURE tool.
"""

URL = str
"""This type should be used wherever a URL is the value of the variable."""

PureToken = str
"""The Pure Token.

It will not have a special schema.
"""

PureRecord = dict
"""The record which will be imported from pure.

This record has to be a dict (json).
"""

FilePath = str
"""The path to the file on the local machine."""

EmailAddress = str
"""The email address.

The address does not have to have a special format, but it has to be an email.
"""

PureUsername = str
"""The pure username which will be used to download files.

It will not have special schema. It is the name which will be created in PURE.
"""

PurePassword = str
"""The pure password which will be used to download files.

It will not have special schema. It is the password which will be created in PURE.
"""


@dataclass
class PureConfigs:
    """Configs for PURE."""

    endpoint: URL
    token: PureToken
    username: PureUsername
    password: PurePassword
    user_email: EmailAddress
    recipients: list[EmailAddress]
    sender: EmailAddress

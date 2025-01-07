# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REST config."""


from dataclasses import dataclass

from ..types import URL, PureToken


@dataclass
class PureRESTConfig:
    """Pure rest config."""

    endpoint: URL = ""
    token: PureToken = ""

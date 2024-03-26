# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services."""

from .config import PureRESTServiceConfig
from .decorators import build_service
from .services import PureRESTService

__all__ = (
    "PureRESTService",
    "PureRESTServiceConfig",
    "build_service",
)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services configs."""

from dataclasses import dataclass

from ..records import PureAPI, PureRESTConfig


@dataclass
class PureRESTServiceConfig(PureRESTConfig):
    """Pure REST service config."""

    api_cls: type[PureAPI] = PureAPI

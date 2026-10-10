# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services configs."""

from dataclasses import dataclass

from ..records import PureAPI, PureRESTConfig


@dataclass
class PureRESTServiceConfig(PureRESTConfig):
    """Pure REST service config."""

    api_cls: type[PureAPI] = PureAPI

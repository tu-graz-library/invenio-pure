# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""REST config."""

from dataclasses import dataclass

from ..types import URL, PureToken


@dataclass
class PureRESTConfig:
    """Pure rest config."""

    endpoint: URL = ""
    token: PureToken = ""

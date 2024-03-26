# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Technische Universität Graz
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REST errors."""

from .types import PureRecord


class PureRuntimeError(RuntimeError):
    """Pure runtime error."""

    def __init__(self, record: PureRecord) -> None:
        """Construct for pure runtime error."""
        self.record = record


class PureAPIError(Exception):
    """Pure API error class."""

    def __init__(self, code: int, msg: str) -> None:
        """Construct for pure api error."""
        super().__init__(f"Pure API error code={code} msg='{msg}'")

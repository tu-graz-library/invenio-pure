# SPDX-FileCopyrightText: 2022-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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

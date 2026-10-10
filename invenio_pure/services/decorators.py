# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services decorators."""

from collections.abc import Callable
from functools import wraps
from typing import Concatenate

from .config import PureRESTServiceConfig
from .services import PureRESTService


def build_service[**P, T](
    func: Callable[Concatenate[PureRESTService, P], T],
) -> Callable[P, T]:
    """Decorate to build the services."""

    @wraps(func)
    def build(*args: P.args, **kwargs: P.kwargs) -> T:
        endpoint = str(kwargs.pop("endpoint"))
        token = str(kwargs.pop("token"))

        config = PureRESTServiceConfig(endpoint, token)
        pure_service = PureRESTService(config=config)

        return func(pure_service, *args, **kwargs)

    return build

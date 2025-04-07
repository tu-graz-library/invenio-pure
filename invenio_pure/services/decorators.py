# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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

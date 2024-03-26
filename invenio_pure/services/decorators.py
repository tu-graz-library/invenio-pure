# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services decorators."""


from collections.abc import Callable
from functools import wraps
from typing import Any

from .config import PureRESTServiceConfig
from .services import PureRESTService


def build_service(f: Callable) -> Callable:
    """Decorate to build the services."""

    @wraps(f)
    def build(*_: dict, **kwargs: dict) -> Any:  # noqa: ANN401
        endpoint = kwargs.pop("endpoint")
        token = kwargs.pop("token")
        username = kwargs.pop("username")
        password = kwargs.pop("password")

        config = PureRESTServiceConfig(endpoint, token, username, password)
        kwargs["pure_service"] = PureRESTService(config)

        return f(**kwargs)

    return build

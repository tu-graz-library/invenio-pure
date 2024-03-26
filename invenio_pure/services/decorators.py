# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services decorators."""


from collections.abc import Callable
from functools import wraps
from typing import TypedDict, Unpack

from .config import PureRESTServiceConfig
from .services import PureRESTService


class KwargsDict(TypedDict, total=False):
    endpoint: str
    token: str
    username: str
    password: str
    user_email: str
    pure_id: str
    no_color: bool
    pure_service: PureRESTService  # not nice, try to remove that from here, mypy


def build_service[T](func: Callable[..., T]) -> Callable:
    """Decorate to build the services."""

    @wraps(func)
    def build(*_: dict, **kwargs: Unpack[KwargsDict]) -> T:
        endpoint = kwargs.pop("endpoint")
        token = kwargs.pop("token")
        username = kwargs.pop("username")
        password = kwargs.pop("password")

        config = PureRESTServiceConfig(endpoint, token, username, password)

        kwargs["pure_service"] = PureRESTService(config=config)

        return func(**kwargs)

    return build

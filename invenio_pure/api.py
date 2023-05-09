# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API functions of the pure connector."""


from collections.abc import Callable

from invenio_records_resources.services.records.results import RecordItem

from .types import PureConfigs, PureRecord
from .utils import download_file, get_research_output_count, get_research_outputs


def import_from_pure(
    import_func: Callable,
    pure_record: PureRecord,
    configs: PureConfigs,
) -> RecordItem:
    """Import record from pure."""
    return import_func(pure_record, configs, download_file)


def pure_records(configs: dict) -> None:
    """Yield records from pure."""
    research_count = get_research_output_count(configs.endpoint, configs.token)
    size = 100
    offset = 0

    while research_count > 0:
        research_output = get_research_outputs(
            configs.endpoint,
            configs.token,
            size,
            offset,
        )

        yield from research_output

        offset += size
        research_count -= size

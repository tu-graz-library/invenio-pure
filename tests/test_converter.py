# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Converter tests."""
import json
from os.path import dirname, join

from invenio_rdm_pure.converter import Marc21Record, Pure2Marc21


def load_json(filename):
    """Load JSON file as dict."""
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


def test_conversion():
    """Test conversion of a Pure record with all attributes."""
    converter = Pure2Marc21()
    pure_json = load_json(join("data", "pure_record_fake.json"))
    record = Marc21Record()
    converter.convert(pure_json, record)
    marc21_xml = record.to_xml_string()

    assert Marc21Record.is_valid_marc21_xml_string(marc21_xml)

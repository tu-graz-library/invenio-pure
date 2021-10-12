# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz
#
# invenio-rdm-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Converter Module to facilitate conversion of metadata."""
import json
import os

import typecheck as tc
from invenio_records_marc21.services import Marc21Metadata


class Converter(object):
    """Converter base class to convert one format into another."""

    def __init__(self):
        """Default Constructor of the class."""
        # Cache iso639-3 language codes to dict
        self.languages = self.initialize_languages()

    def initialize_languages(self) -> dict:
        """Initialize language cache dictionary."""
        path = os.path.join(os.path.dirname(__file__), "../data", "iso6393.json")

        with open(path) as fp:
            languages = filter(lambda obj: "iso6393" in obj, json.load(fp))

        return {language["name"]: language["iso6393"] for language in languages}

    def convert(self, value: object, record: Marc21Metadata):
        """Convert record from Pure JSON format to MARC21XML."""
        for attribute, value in value.items():
            self.convert_attribute(attribute, value, record)

    def convert_attribute(self, attribute: str, value: object, record: Marc21Metadata):
        """Traverse first level elements of dictionary and extract necessary attributes."""
        convert_function = getattr(self, f"convert_{attribute}", lambda *args: None)
        convert_function(value, record)


class Pure2Marc21(Converter):
    """Pure to marc21 converter class."""

    @tc.typecheck
    def convert_abstract(self, value: dict, record: Marc21Metadata):
        """Add the abstract to the Marc21Metadata."""
        for abstract in value["text"]:
            record.emplace_field(tag="520", code="a", value=abstract["value"])

    @tc.typecheck
    def convert_additionalLinks(self, value: list, record: Marc21Metadata):
        """Add the additionalLinks attribute to the Marc21Metadata."""
        for link in value:
            if "url" in link:
                record.emplace_field(
                    tag="856", ind1="4", ind2="1", code="u", value=link["url"]
                )

    @tc.typecheck
    def convert_bibliographicalNote(self, value: dict, record: Marc21Metadata):
        """Add the bibliographicalNote attribute to the Marc21Metadata."""
        for text in value["text"]:
            record.emplace_field(tag="500", code="a", value=text["value"])

    @tc.typecheck
    def convert_edition(self, value: str, record: Marc21Metadata):
        """Add the edition attribute to the Marc21Metadata."""
        record.emplace_field(tag="250", code="a", value=value)

    @tc.typecheck
    def convert_electronicIsbns(self, value: list, record: Marc21Metadata):
        """Add the electronicIsbns attribute to the Marc21Metadata."""
        record.emplace_field(tag="020", code="a", value=str(value[0]).strip())

    @tc.typecheck
    def convert_event(self, value: dict, record: Marc21Metadata):
        """Add the event attribute to the Marc21Metadata."""
        for event_name in value["name"]["text"]:
            record.emplace_field(
                tag="711", ind1="2", code="a", value=event_name["value"]
            )

    @tc.typecheck
    def convert_isbns(self, value: list, record: Marc21Metadata):
        """Add the isbns attribute to the Marc21Metadata."""
        for isbn in value:
            record.emplace_field(tag="020", code="a", value=isbn)

    @tc.typecheck
    def convert_journalAssociation(self, value: dict, record: Marc21Metadata):
        """Add the journalAssociation attribute to the Marc21Metadata."""
        value = value["title"]["value"]
        record.emplace_field(tag="773", ind1="0", ind2="8", code="t", value=value)

    @tc.typecheck
    def convert_journalNumber(self, value: str, record: Marc21Metadata):
        """Add the journalNumber attribute to the Marc21Metadata."""
        record.emplace_field(tag="773", ind1="0", ind2="8", code="g", value=value)

    @tc.typecheck
    def convert_keywordGroups(self, value: list, record: Marc21Metadata):
        """Add the keywordGroups attribute to the Marc21Metadata."""
        for item in value:
            keyword_group = KeywordGroup()
            keyword_group.convert(item, record)

    @tc.typecheck
    def convert_language(self, value: dict, record: Marc21Metadata):
        """Add the language attribute to the Marc21Metadata."""
        for locale in value["term"]["text"]:
            language = locale["value"]
            language_iso6393 = self.languages[language]
            record.emplace_field(tag="041", code="a", value=language_iso6393)

    @tc.typecheck
    def convert_managingOrganisationalUnit(self, value: dict, record: Marc21Metadata):
        """Add the managingOrganisationalUnit attribute to the Marc21Metadata."""
        for locale in value["name"]["text"]:
            record.emplace_unique_field(
                tag="100", ind1="1", code="u", value=locale["value"]
            )
            record.emplace_unique_field(
                tag="700", ind1="1", code="u", value=locale["value"]
            )

    @tc.typecheck
    def convert_numberOfPages(self, value: int, record: Marc21Metadata):
        """Add the numberOfPages attribute to the Marc21Metadata."""
        record.emplace_field(tag="300", code="a", value=str(value))

    @tc.typecheck
    def convert_organisationalUnits(self, value: list, record: Marc21Metadata):
        """Add the organisationalUnits attribute to the Marc21Metadata."""
        for o_unit in value:
            for locale in o_unit["name"]["text"]:
                record.emplace_unique_field(
                    tag="100", ind1="1", code="u", value=locale["value"]
                )
                record.emplace_unique_field(
                    tag="700", ind1="1", code="u", value=locale["value"]
                )

    @tc.typecheck
    def convert_pages(self, value: str, record: Marc21Metadata):
        """Add the pages attriute to the Marc21Metadata."""
        pages = value
        record.emplace_field(tag="300", code="a", value=pages)

    @tc.typecheck
    def convert_patentNumber(self, value: str, record: Marc21Metadata):
        """Add the patentNumber attribute to the Marc21Metadata."""
        record.emplace_field(tag="013", code="a", value=value)

    @tc.typecheck
    def convert_peerReview(self, value: bool, record: Marc21Metadata):
        """Add the peerReview attribute to the Marc21Metadata."""
        if value:
            status = "Refereed/Peer-reviewed"
            record.emplace_field(tag="500", code="a", value=status)

    @tc.typecheck
    def convert_placeOfPublication(self, value: str, record: Marc21Metadata):
        """Add the placeOfPublication attribute to the Marc21Metadata."""
        record.emplace_field(tag="264", code="a", value=value)

    @tc.typecheck
    def convert_publicationSeries(self, value: list, record: Marc21Metadata):
        """Add the publicationSeries attribute to the Marc21Metadata."""
        for series in value:
            record.emplace_field(tag="490", ind1="0", code="a", value=series["name"])

    @tc.typecheck
    def convert_publicationStatuses(self, value: list, record: Marc21Metadata):
        """Add the publicationStatuses attribute to the Marc21Metadata."""

        for entry in value:
            publication_status = PublicationStatus()
            publication_status.convert(entry, record)

    @tc.typecheck
    def convert_publisher(self, value: dict, record: Marc21Metadata):
        """Add the publisher attribute to the Marc21Metadata."""
        for text in value["name"]["text"]:
            record.emplace_field(tag="264", code="b", value=text["value"])

    @tc.typecheck
    def convert_relatedProjects(self, value: list, record: Marc21Metadata):
        """Add the relatedProjects attribute to the Marc21Metadata."""
        for entry in value:
            for locale in entry["name"]["text"]:
                record.emplace_field(tag="536", code="a", value=locale["value"])

    @tc.typecheck
    def convert_subTitle(self, value: dict, record: Marc21Metadata):
        """Add the subTitle attribute to the Marc21Metadata."""
        record.emplace_field(
            tag="245", ind1="1", ind2="0", code="b", value=value["value"]
        )

    @tc.typecheck
    def convert_title(self, value: dict, record: Marc21Metadata):
        """Add the title attribute to the Marc21Metadata."""
        record.emplace_field(
            tag="245", ind1="1", ind2="0", code="a", value=value["value"]
        )

    @tc.typecheck
    def convert_volume(self, value: str, record: Marc21Metadata):
        """Add the volume attribute to the Marc21Metadata."""
        record.emplace_field(tag="490", ind1="0", code="a", value=value)
        record.emplace_field(tag="773", ind1="0", ind2="8", code="g", value=value)


class KeywordGroup(Converter):
    """Class to convert the keywordgroup attribute."""

    @tc.typecheck
    def convert_keywordContainers(self, value: list, record: Marc21Metadata):
        """Add keywords."""
        for item in value:
            self.convert(item, record)

    @tc.typecheck
    def convert_freeKeywords(self, value: list, record: Marc21Metadata):
        """Add free keywords."""
        for free_keyword in value:
            for word in free_keyword["freeKeywords"]:
                record.emplace_field(tag="650", ind2="4", code="g", value=word)

    @tc.typecheck
    def convert_structuredKeyword(self, value: dict, record: Marc21Metadata):
        """Add free keywords."""
        for word in value["term"]["text"]:
            record.emplace_field(tag="650", ind2="4", code="a", value=word["value"])


class PublicationStatus(Converter):
    """Class to convert publication status."""

    @tc.typecheck
    def convert_publicationDate(self, value: dict, record: Marc21Metadata):
        record.emplace_field(tag="264", code="c", value=value["year"])

    @tc.typecheck
    def convert_publicationStatus(self, value: dict, record: Marc21Metadata):
        for text in value["term"]["text"]:
            record.emplace_field(tag="250", code="a", value=text["value"])

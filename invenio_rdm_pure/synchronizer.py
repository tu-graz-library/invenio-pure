# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Technische Universität Graz
#
# invenio-rdm-pure is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Synchronizer module to facilitate record synchronization between Invenio and Pure."""

from os.path import basename, dirname, isabs, join  # isfile,
from pathlib import Path
from typing import List

from flask import current_app
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access.permissions import any_user
from invenio_db import db
from invenio_files_rest.models import ObjectVersion
from invenio_records_marc21.services import (  # Metadata,
    Marc21DraftFilesService,
    Marc21Metadata,
    Marc21RecordService,
    RecordItem,
)

from ..converter import Pure2Marc21
from ..pure.utils import (
    download_pure_file,
    get_research_output_count,
    get_research_outputs,
)
from ..utils import get_user_id, send_email  # get_dates_in_span,


class Synchronizer(object):
    """Synchronizer class to facilitate record synchronization between Invenio and Pure."""

    @with_appcontext
    def __init__(
        self,
        api_url: str = "",
        api_key: str = "",
        username: str = "",
        password: str = "",
        user_email: str = "",
        user_password: str = "",
        responsible_email: str = "",
    ):
        """Default Constructor of the Synchronizer class.

        Make sure, that the access urls, usernames, passwords etc. are working
        before going ahead, otherwise throw an error."""

        def ifelse(a: str, b: str) -> str:
            return a if a else b

        def get(key: str) -> str:
            return current_app.config.get(key)

        self.api_url = ifelse(api_url, get("PURE_API_URL"))
        self.api_key = ifelse(api_key, get("PURE_API_KEY"))
        self.username = ifelse(username, get("PURE_USERNAME"))
        self.password = ifelse(password, get("PURE_PASSWORD"))
        self.user_email = ifelse(user_email, get("PURE_USER_EMAIL"))
        self.user_password = ifelse(user_password, get("PURE_USER_PASSWORD"))
        self.user_id = get_user_id(user_email, user_password)
        self.responsible_email = ifelse(
            responsible_email, get("PURE_RESPONSIBLE_EMAIL")
        )

    def run_initial_synchronization(self) -> None:
        """Run the initial synchronization.

        In this case the database is empty.
        """
        self.run_initial_research_output_synchronization()

    def run_initial_research_output_synchronization(
        self, granularity: int = 100
    ) -> None:
        """Run initial synchronization for all research outputs."""
        research_count = get_research_output_count(self.api_key, self.api_url)
        assert research_count != -1, "Failed to get research output count"

        for job_counter in range(0, (research_count // granularity) + 1):
            if job_counter == research_count // granularity:
                current_granularity = research_count - job_counter * granularity
            else:
                current_granularity = granularity

            self.synchronize_research_outputs(
                current_app._get_current_object(),
                current_granularity,
                job_counter * granularity,
            )

    def synchronize_research_outputs(self, size: int, offset: int) -> None:
        """Synchronize a series of research outputs.

        Pure API identifies a series by the following parameters:
        The *size* parameter defines the length of the series.
        The *offset* parameter defines the offset of the series.
        """
        research_outputs = get_research_outputs(
            self.api_key, self.api_url, size, offset
        )

        converter = Pure2Marc21()
        for research_output in research_outputs:
            try:
                marc21_record = Marc21Metadata()
                converter.convert(research_output, marc21_record)

                file_paths = self.download_record_files(research_output)
                self.create_record(marc21_record, file_paths)
                self.send_pure_delete_requests(research_output, file_paths)
            except RuntimeError as exc:
                current_app.logger.exception(exc)

    def send_pure_delete_requests(
        self, research_output: dict, file_paths: List[str]
    ) -> None:
        """Send delete requests to Pure responsible."""
        for file_path in file_paths:
            send_email(
                research_output["uuid"],
                basename(file_path),
                self.user_email,
                self.user_password,
                self.responsible_email,
            )

    def create_record(self, record: Marc21Metadata, file_paths: List[str]) -> None:
        """Create Invenio record from Marc21XML string."""
        identity = Identity(self.user_id)
        identity.provides.add(any_user)

        service = Marc21RecordService()
        draft = service.create(metadata=record, identity=identity)

        self.attach_files_to_draft(file_paths, draft)
        self.delete_record_files(file_paths)
        service.publish(id_=draft.id, identity=identity)

    def download_record_files(
        self, record: dict, destination_path: str = "temp"
    ) -> List:
        """Download files associated with record into path defined in destination path."""
        file_paths = []
        if not isabs(destination_path):
            destination_path = join(dirname(__file__), destination_path)

        Path(destination_path).mkdir(parents=True, exist_ok=True)
        if "electronicVersions" not in record:
            return file_paths

        for electronic_version in record["electronicVersions"]:
            if "file" in electronic_version:
                file_path = download_pure_file(
                    electronic_version["file"]["fileURL"],
                    self.username,
                    self.password,
                    destination_path,
                    electronic_version["file"]["file_path"],
                )
                file_paths.append(file_path)
        return file_paths

    def attach_files_to_draft(self, file_paths: List[str], draft: RecordItem) -> None:
        """Attach files to given record."""
        identity = Identity(self.user_id)
        identity.provides.add(any_user)
        service = Marc21DraftFilesService()

        if file_paths:
            draft = service.update_files_options(
                id_=draft.id, identity=identity, data={"enabled": False}
            )

        for file_path in file_paths:
            filep = open(file_path, "rb")
            ObjectVersion.create(
                str(draft._record.bucket_id), str(basename(file_path)), stream=filep
            )
            filep.close()
            db.session.commit()

    def delete_record_files(self, file_paths: List[str]) -> None:
        """Delete files with given path."""
        for file_path in file_paths:
            Path(file_path).unlink(missing_ok=True)


import json
from typing import Dict

from ..lib.log_tools import make_default_logger

from ..lib.log_tools import make_default_logger
from .reports import BaseReport


logger = make_default_logger()

class ACMSAttachmentPage(BaseReport):
    """Parse ACMS attachment pages' JSON."""

    def __init__(self, court_id, pacer_session=None):
        super().__init__(court_id, pacer_session)

    def _parse_text(self, text):
        """Store the ACMS JSON

        This does not, in fact, actually *parse* the data, it
        stores it for subsequent parsing, which happens in
        data().

        :param text: A unicode object
        :return: None
        """
        self._acms_json = json.loads(text)


    @property
    def data(self) -> Dict:
        case_details = self._acms_json["caseDetails"]
        docket_entry = self._acms_json["docketEntry"]
        result = {
            "pacer_doc_id": docket_entry["docketEntryId"],
            "pacer_case_id": case_details["caseId"],
            "attachments": [],
        }

        for row in self._acms_json["docketEntryDocuments"]:
            result["attachments"].append(
                {
                    "attachment_number": int(row['documentNumber']),
                    "description": row['name'],
                    "page_count": row['billablePages'],
                    "pacer_doc_id": docket_entry["docketEntryId"],
                    "acms_document_guid": row['docketDocumentDetailsId']
                }
            )

        return result

import json
import pprint
import sys

from typing import Dict

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
                    "attachment_number": int(row["documentNumber"]),
                    "description": row["name"],
                    "page_count": row["billablePages"],
                    "pacer_doc_id": docket_entry["docketEntryId"],
                    "acms_document_guid": row["docketDocumentDetailsId"],
                }
            )

        return result


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m juriscraper.pacer.acms_attachment_page filepath"
        )
        print("Please provide a path to an HTML file to parse.")
        sys.exit(1)
    report = ACMSAttachmentPage(
        "cand"
    )  # Court ID is only needed for querying.
    filepath = sys.argv[1]
    print(f"Parsing HTML file at {filepath}")
    with open(filepath) as f:
        text = f.read()
    report._parse_text(text)
    print([x for x in report._acms_json])
    pprint.pprint(report.data, indent=2)


if __name__ == "__main__":
    main()

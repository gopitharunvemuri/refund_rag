import re
from typing import Any


class ReferenceResolver:
    """
    Builds a document-level index of Docling elements.

    The index maps each element's self_ref to its
    original Docling object.
    """

    COLLECTIONS = (
        "texts",
        "tables",
        "groups",
        "pictures",
        "key_value_items",
        "form_items",
    )

    def __init__(
    self,
    document: dict[str, Any],
    document_id: str
):
        self.document_id = document_id
        self.audit_log: list[dict[str, Any]] = []
        self.document = document
        self.reference_index: dict[str, dict[str, Any]] = {}
        self.missing_self_refs: list[dict[str, str]] = []
        self.build_index()

    def build_index(self) -> None:
        """
        Build an index using self_ref from each
        supported Docling collection.
        """

        for collection_name in self.COLLECTIONS:
            elements = self.document.get(collection_name, [])

            if not isinstance(elements, list):
                raise ValueError(
                    f"Expected a list for collection: {collection_name}"
                )

            for element in elements:
                if not isinstance(element, dict):
                    raise ValueError(
                        f"Invalid element in collection: {collection_name}"
                    )
                # print(element)
                self_ref = element.get("self_ref")

                if not self_ref:
                    self.missing_self_refs.append({
                        "collection": collection_name,
                        "label": str(element.get("label", "unknown"))
                    })
                    continue

                if self_ref in self.reference_index:
                    raise ValueError(
                        f"Duplicate Docling reference found: {self_ref}"
                    )

                self.reference_index[self_ref] = element

    def get_index(self) -> dict[str, dict[str, Any]]:
        """
        Return the completed reference index.
        """

        return self.reference_index

    def get_index_count(self) -> int:
        """
        Return the total number of indexed elements.
        """

        return len(self.reference_index)
    def get_missing_self_refs(self) -> list[dict[str, str]]:
        return self.missing_self_refs

    def validate_reference(self, reference: str) -> dict[str, Any]:
        """
        Validate a Docling reference without resolving it.
        """

        if not isinstance(reference, str) or not reference:
            return {
                "valid": False,
                "reference": reference,
                "reason": "Reference must be a non-empty string"
            }

        pattern = r"^#/([a-zA-Z0-9_]+)/([0-9]+)$"

        match = re.fullmatch(pattern, reference)

        if not match:
            return {
                "valid": False,
                "reference": reference,
                "reason": "Invalid reference format"
            }

        collection_name = match.group(1)

        if collection_name not in self.COLLECTIONS:
            return {
                "valid": False,
                "reference": reference,
                "reason": "Unsupported collection"
            }

        if reference not in self.reference_index:
            return {
                "valid": False,
                "reference": reference,
                "reason": "Reference does not exist in index"
            }

        return {
            "valid": True,
            "reference": reference,
            "collection": collection_name,
            "reason": None
        }
    
    
    def resolve_reference(self, reference: str) -> dict[str, Any]:
        """
        Resolve a Docling reference and record the outcome.
        """

        validation_result = self.validate_reference(reference)

        if not validation_result["valid"]:

            self.audit_log.append({
                "document_id": self.document_id,
                "reference": reference,
                "status": "failed",
                "element_type": None,
                "error": validation_result["reason"]
            })

            raise ValueError(
                f"Cannot resolve reference '{reference}': "
                f"{validation_result['reason']}"
            )

        resolved_element = self.reference_index[reference]

        self.audit_log.append({
            "document_id": self.document_id,
            "reference": reference,
            "status": "success",
            "element_type": resolved_element.get("label"),
            "error": None
        })

        return resolved_element

    def get_audit_log(self) -> list[dict[str, Any]]:
        """Return all reference resolution audit records."""

        return list(self.audit_log)


    def get_audit_summary(self) -> dict[str, int]:
        """Return success and failure counts."""

        successful = sum(
            record["status"] == "success"
            for record in self.audit_log
        )

        failed = sum(
            record["status"] == "failed"
            for record in self.audit_log
        )

        return {
            "total_attempts": len(self.audit_log),
            "successful": successful,
            "failed": failed
        }




from pathlib import Path

from structured.docling_reader import DoclingReader


PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DOCUMENTS_DIR = (
    PROJECT_DIR / "parsed_documents" / "raw"
)


def main():

    reader = DoclingReader(RAW_DOCUMENTS_DIR)

    document = reader.read_document(
        "NX-FIN-POL-012"
    )

    resolver = ReferenceResolver(
        document,
        document_id="NX-FIN-POL-012"
    )

    test_references = [
        "#/texts/0",
        "#/tables/0",
        "#/groups/0",
    ]

    print("\nREFERENCE RESOLUTION TEST")
    print("-------------------------")

    for reference in test_references:

        element = resolver.resolve_reference(reference)

        print("\nReference:", reference)
        print("Label:", element.get("label"))
        print("Self reference:", element.get("self_ref"))
        print("Page provenance:", element.get("prov"))

        if "text" in element:
            print("Text:", element.get("text")[:200])

        elif "data" in element:
            print("Data keys:", list(element["data"].keys()))


    print("\nTesting invalid reference:")

    try:
        resolver.resolve_reference("#/texts/9999")

    except ValueError as error:
        print("Correctly rejected:", error)

    print("\nAUDIT SUMMARY")
    print("-------------")

    print(resolver.get_audit_summary())

    print("\nAUDIT RECORDS")
    print("-------------")

    for record in resolver.get_audit_log():
        print(record)
if __name__ == "__main__":
    main()

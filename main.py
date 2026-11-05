from pathlib import Path

from config.documents import DOCUMENTS
from ingestion.document_loader import (
    inspect_pdf,
    DocumentValidationError
)
from ingestion.document_registry import (
    DocumentRegistry,
    RegistryError
)


BASE_DIR = Path(__file__).resolve().parent

INCOMING_DIR = BASE_DIR / "data"

REGISTRY_PATH = (
    BASE_DIR / "registry" / "document_registry.json"
)


def run_ingestion():

    registry = DocumentRegistry(REGISTRY_PATH)

    print("\n======================================")
    print(" ENTERPRISE POLICY DOCUMENT INGESTION")
    print("======================================\n")

    for document in DOCUMENTS:

        print(f"\nProcessing: {document['document_id']}")
        print(f"Document: {document['document_name']}")

        file_path = INCOMING_DIR / document["file_name"]

        try:
            # Step 1: Validate and inspect the PDF.
            file_metadata = inspect_pdf(
                file_path,
                INCOMING_DIR
            )

            # Step 2: Register the document.
            result = registry.register_document(
                document,
                file_metadata
            )

            print(f"Status: {result}")
            print(f"SHA-256: {file_metadata['file_hash']}")
            print(f"File size: {file_metadata['file_size_bytes']} bytes")
            print(f"Pages: {file_metadata['page_count']}")

        except (DocumentValidationError, RegistryError) as exc:

            print(f"FAILED: {exc}")

        except OSError as exc:

            print(f"FILE ERROR: {exc}")

    print("\n======================================")
    print(" REGISTRY SUMMARY")
    print("======================================")

    registered_documents = registry.get_all_documents()

    for item in registered_documents:

        print(
            f"{item['document_id']} | "
            f"Version: {item['version']} | "
            f"Status: {item['status']}"
        )

    print(f"\nTotal registered documents: {len(registered_documents)}")


if __name__ == "__main__":
    run_ingestion()
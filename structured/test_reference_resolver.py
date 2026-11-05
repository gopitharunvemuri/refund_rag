
from pathlib import Path

from structured.docling_reader import DoclingReader
from structured.reference_resolver import ReferenceResolver


PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DOCUMENTS_DIR = (
    PROJECT_DIR / "parsed_documents" / "raw"
)

DOCUMENT_IDS = [
    "NX-FIN-POL-012",
    "NX-FIN-POL-013",
    "NX-FIN-POL-014",
]


def test_document(document_id, reader):

    print(f"\n{'=' * 55}")
    print(f"TESTING: {document_id}")
    print("=" * 55)

    document = reader.read_document(document_id)

    resolver = ReferenceResolver(
        document,
        document_id=document_id
    )

    index = resolver.get_index()

    # Check duplicate references
    duplicate_count = (
        len(index) - len(set(index.keys()))
    )

    # Check missing self references
    missing_refs = resolver.get_missing_self_refs()

    # Attempt to resolve every indexed reference
    successful_resolutions = 0
    failed_resolutions = 0

    for reference in index.keys():

        try:
            resolver.resolve_reference(reference)
            successful_resolutions += 1

        except ValueError:
            failed_resolutions += 1

    summary = resolver.get_audit_summary()

    print("\nINDEX STATISTICS")
    print("Total indexed elements:", len(index))
    print("Duplicate references:", duplicate_count)
    print("Missing self_ref elements:", len(missing_refs))

    print("\nRESOLUTION STATISTICS")
    print("Successful:", successful_resolutions)
    print("Failed:", failed_resolutions)
    print("Audit attempts:", summary["total_attempts"])

    print("\nMISSING REFERENCE DETAILS")

    if missing_refs:
        for item in missing_refs:
            print(item)
    else:
        print("No missing self_ref elements.")

    # Basic test assertions
    assert duplicate_count == 0
    assert failed_resolutions == 0
    assert summary["total_attempts"] == len(index)
    assert summary["successful"] == len(index)
    assert summary["failed"] == 0

    print("\nRESULT: PASSED")

    return {
        "document_id": document_id,
        "indexed": len(index),
        "missing_self_refs": len(missing_refs),
        "resolved": successful_resolutions,
        "failed": failed_resolutions,
        "status": "PASSED"
    }


def main():

    reader = DoclingReader(RAW_DOCUMENTS_DIR)

    results = []

    for document_id in DOCUMENT_IDS:

        result = test_document(document_id, reader)
        results.append(result)

    print(f"\n{'=' * 55}")
    print("FINAL REFERENCE RESOLVER REPORT")
    print("=" * 55)

    for result in results:
        print(result)

    print("\nALL DOCUMENTS PASSED REFERENCE RESOLVER TESTS")


if __name__ == "__main__":
    main()

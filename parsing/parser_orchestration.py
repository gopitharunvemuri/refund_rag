import json

from pathlib import Path

from parsing.pdf_parser import (
    PDFparser,
    PDFParsingError
)


BASE_DIR = Path(__file__).resolve().parent.parent

INCOMING_DIR = BASE_DIR / "data"

RAW_OUTPUT_DIR = BASE_DIR / "parsed_documents" / "raw"

REPORT_DIR = BASE_DIR / "parsed_documents" / "reports"

REGISTRY_PATH = (
    BASE_DIR / "registry" / "document_registry.json"
)


def load_registry():

    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(
            "Document registry does not exist. "
            "Complete Step 1 first."
        )

    with REGISTRY_PATH.open(
        "r",
        encoding="utf-8"
    ) as file:

        registry = json.load(file)

    return registry["documents"]


def run_parsing():

    documents = load_registry()

    parser = PDFparser()

    results = []

    print("\n====================================")
    print(" ENTERPRISE PDF PARSING PIPELINE")
    print("====================================")

    for document in documents:

        document_id = document["document_id"]

        print(f"\nParsing: {document_id}")

        pdf_path = (
            INCOMING_DIR / document["file_name"]
        )

        output_path = (
            RAW_OUTPUT_DIR / f"{document_id}.json"
        )

        try:

            result = parser.parse_document(
                input_path=pdf_path,
                output_path=output_path,
                document_metadata=document
            )

            results.append(result)

            print("Status: SUCCESS")
            print(f"Output: {output_path}")

        except (PDFParsingError, OSError) as exc:

            result = {
                "document_id": document_id,
                "source_file": document["file_name"],
                "parsing_status": "FAILED",
                "error": str(exc)
            }

            results.append(result)

            print(f"Status: FAILED")
            print(f"Error: {exc}")

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = REPORT_DIR / "parsing_report.json"

    with report_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    successful = sum(
        item["parsing_status"] == "SUCCESS"
        for item in results
    )

    failed = len(results) - successful

    print("\n====================================")
    print(" PARSING SUMMARY")
    print("====================================")
    print(f"Total documents: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    run_parsing()
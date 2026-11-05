import json
from pathlib import Path
from datetime import datetime, timezone
from docling.document_converter import DocumentConverter

class PDFParsingError(Exception):
    "Raised when document parsing fails."

class PDFparser:

    def __init__(self):
        self.document_converter = DocumentConverter()

    def parse_document(self, input_path: Path, output_path: Path, document_metadata):
        if not input_path.exists():
            raise PDFParsingError(
                f"PDF not found in the address {input_path}"
            )
        if input_path.suffix.lower() != ".pdf":
            raise PDFParsingError(
                f"Only PDF files are allowed."
            )
        
        try:
            converted_document = self.document_converter.convert(str(input_path))
            parsed_document = converted_document.document.export_to_dict()
            if not isinstance(parsed_document, dict):
                raise PDFParsingError(
                    "Parser returned an invalid document structure."
                )

            if not parsed_document:
                raise PDFParsingError(
                    "Parser returned an empty document."
                )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )
            with output_path.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    parsed_document,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            return {
                "document_id": document_metadata["document_id"],
                "document_version": document_metadata["version"],
                "source_file": input_path.name,
                "parsed_file": str(output_path),
                "parsing_status": "SUCCESS",
                "parser": "DOCLING",
                "parsed_timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "top_level_keys": list(
                    parsed_document.keys()
                )
            }

        except PDFParsingError:
            raise

        except Exception as exc:
            raise PDFParsingError(
                f"Failed to parse {input_path.name}: {exc}"
            ) from exc
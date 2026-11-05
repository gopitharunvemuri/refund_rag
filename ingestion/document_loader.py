import hashlib
from pathlib import Path

from pypdf import PdfReader


class DocumentValidationError(Exception):
    """Raised when a source document fails validation."""


def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 checksum without loading the whole file."""

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def inspect_pdf(file_path: Path, incoming_dir: Path) -> dict:
    """
    Validate a PDF and collect its basic registration information.

    This function does not extract document text or create chunks.
    """

    incoming_dir = incoming_dir.resolve()
    file_path = file_path.resolve()

    # Prevent files outside the incoming directory from being registered.
    if not file_path.is_relative_to(incoming_dir):
        raise DocumentValidationError(
            "File is outside the approved incoming directory."
        )

    if not file_path.exists():
        raise DocumentValidationError(
            f"File does not exist: {file_path.name}"
        )

    if not file_path.is_file():
        raise DocumentValidationError(
            "The supplied path is not a file."
        )

    if file_path.suffix.lower() != ".pdf":
        raise DocumentValidationError(
            "Only PDF files are accepted."
        )

    file_size = file_path.stat().st_size

    if file_size == 0:
        raise DocumentValidationError("PDF file is empty.")

    # Check the PDF signature.
    with file_path.open("rb") as file:
        header = file.read(5)

    if header != b"%PDF-":
        raise DocumentValidationError(
            "File does not have a valid PDF header."
        )

    # Perform basic structural validation.
    try:
        reader = PdfReader(str(file_path), strict=True)

        if reader.is_encrypted:
            raise DocumentValidationError(
                "Encrypted PDFs are not supported by this ingestion step."
            )

        page_count = len(reader.pages)

        if page_count == 0:
            raise DocumentValidationError(
                "PDF contains no pages."
            )

    except DocumentValidationError:
        raise

    except Exception as exc:
        raise DocumentValidationError(
            f"PDF structure validation failed: {exc}"
        ) from exc

    return {
        "file_name": file_path.name,
        "file_size_bytes": file_size,
        "file_hash": calculate_sha256(file_path),
        "page_count": page_count,
        "relative_path": str(file_path.relative_to(
            Path.cwd().resolve()
        ))
    }
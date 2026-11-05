import json
import os
import tempfile

from datetime import datetime, timezone
from pathlib import Path


class RegistryError(Exception):
    """Raised when document registration fails."""


class DocumentRegistry:

    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.registry_path.exists():
            self._save({"documents": []})

    def _load(self) -> dict:
        try:
            with self.registry_path.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise RegistryError("Registry must be a JSON object.")

            if not isinstance(data.get("documents"), list):
                raise RegistryError(
                    "Registry must contain a documents list."
                )

            return data

        except json.JSONDecodeError as exc:
            raise RegistryError(
                "Registry JSON is corrupted."
            ) from exc

    def _save(self, data: dict) -> None:
        """Write atomically so an interrupted write does not corrupt the registry."""

        self.registry_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.registry_path.parent,
                delete=False
            ) as temp_file:

                json.dump(
                    data,
                    temp_file,
                    indent=4,
                    ensure_ascii=False
                )

                temp_file.flush()
                os.fsync(temp_file.fileno())
                temp_path = Path(temp_file.name)

            os.replace(temp_path, self.registry_path)

        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink()

    def register_document(
        self,
        document_metadata: dict,
        file_metadata: dict
    ) -> str:

        data = self._load()
        documents = data["documents"]

        document_id = document_metadata["document_id"]
        version = document_metadata["version"]
        file_hash = file_metadata["file_hash"]

        # Check whether this exact document version is already registered.
        for existing in documents:

            if (
                existing["document_id"] == document_id
                and existing["version"] == version
            ):

                if existing["file_hash"] == file_hash:
                    return "ALREADY_REGISTERED"

                raise RegistryError(
                    f"{document_id} version {version} already exists "
                    "with a different file hash. "
                    "Do not overwrite an existing policy version."
                )

        record = {
            **document_metadata,
            **file_metadata,
            "status": "REGISTERED",
            "ingestion_timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "effective_to": None
        }

        documents.append(record)

        self._save(data)

        return "REGISTERED"

    def get_all_documents(self) -> list:
        return self._load()["documents"]
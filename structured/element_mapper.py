from typing import Any

from structured.canonical_representation import (
    CanonicalElement,
    SourceInformation,
    ElementStructure,
    ElementMetadata,
)


class ElementMapper:

    def __init__(self, document_id: str):
        self.document_id = document_id

    def map_text_element(
        self,
        element: dict[str, Any],
    ) -> CanonicalElement:

        reference = element["self_ref"]
        label = element.get("label", "other")

        if label not in ("text", "section_header", "page_footer"):
            raise ValueError(
                f"Unsupported text element label: {label}"
            )

        page_numbers = []
        bounding_boxes = []

        for provenance in element.get("prov", []):
            page_number = provenance.get("page_no")

            if page_number is not None:
                page_numbers.append(page_number)

            bbox = provenance.get("bbox")

            if bbox:
                bounding_boxes.append(bbox)

        return CanonicalElement(
            element_id=f"{self.document_id}-{reference.replace('#/', '').replace('/', '-')}",
            document_id=self.document_id,
            element_type = (
                "section_header" if label == "section_header"
                else "other" if label == "page_footer"
                else "text"
            ),
            content=element.get("text", ""),
            source=SourceInformation(
                reference=reference,
                collection="texts",
                page_numbers=page_numbers,
                bounding_boxes=bounding_boxes,
            ),
            structure=ElementStructure(
                parent_reference=(
                    element.get("parent", {}).get("$ref")
                ),
                child_references=[
                    child.get("$ref")
                    for child in element.get("children", [])
                    if child.get("$ref")
                ],
                heading_level=element.get("level"),
            ),
            metadata=ElementMetadata(
                original_label=label,
                content_layer=element.get("content_layer"),
            ),
            raw_data=element,
        )
    def map_list_item(
    self,
    element: dict[str, Any],
) -> CanonicalElement:

        if element.get("label") != "list_item":
            raise ValueError(
                f"Expected list_item, got: {element.get('label')}"
            )

        reference = element["self_ref"]

        page_numbers = []
        bounding_boxes = []

        for provenance in element.get("prov", []):
            page_number = provenance.get("page_no")

            if page_number is not None:
                page_numbers.append(page_number)

            bbox = provenance.get("bbox")

            if bbox:
                bounding_boxes.append(bbox)

        return CanonicalElement(
            element_id=f"{self.document_id}-{reference.replace('#/', '').replace('/', '-')}",
            document_id=self.document_id,
            element_type="list_item",
            content=element.get("text", ""),
            source=SourceInformation(
                reference=reference,
                collection="texts",
                page_numbers=page_numbers,
                bounding_boxes=bounding_boxes,
            ),
            structure=ElementStructure(
                parent_reference=(
                    element.get("parent", {}).get("$ref")
                ),
                enumerated=element.get("enumerated"),
                list_marker=element.get("marker"),
            ),
            metadata=ElementMetadata(
                original_label="list_item",
                content_layer=element.get("content_layer"),
            ),
            raw_data=element,
        )
    
    def map_group(
        self,
        element: dict[str, Any],
    ) -> CanonicalElement:

        reference = element["self_ref"]

        child_references = [
            child.get("$ref")
            for child in element.get("children", [])
            if child.get("$ref")
        ]

        return CanonicalElement(
            element_id=f"{self.document_id}-{reference.replace('#/', '').replace('/', '-')}",
            document_id=self.document_id,
            element_type="group",
            content=None,
            source=SourceInformation(
                reference=reference,
                collection="groups",
            ),
            structure=ElementStructure(
                parent_reference=(
                    element.get("parent", {}).get("$ref")
                ),
                child_references=child_references,
            ),
            metadata=ElementMetadata(
                original_label=element.get("label", "group"),
                content_layer=element.get("content_layer"),
            ),
            raw_data=element,
        )
    
    def map_table(
        self,
        element: dict[str, Any],
    ) -> CanonicalElement:

        if element.get("label") != "table":
            raise ValueError(
                f"Expected table, got: {element.get('label')}"
            )

        reference = element["self_ref"]

        page_numbers = []
        bounding_boxes = []

        for provenance in element.get("prov", []):
            page_number = provenance.get("page_no")

            if page_number is not None:
                page_numbers.append(page_number)

            bbox = provenance.get("bbox")

            if bbox:
                bounding_boxes.append(bbox)

        return CanonicalElement(
            element_id=f"{self.document_id}-{reference.replace('#/', '').replace('/', '-')}",
            document_id=self.document_id,
            element_type="table",
            content=element.get("data", {}),
            source=SourceInformation(
                reference=reference,
                collection="tables",
                page_numbers=page_numbers,
                bounding_boxes=bounding_boxes,
            ),
            structure=ElementStructure(
                parent_reference=(
                    element.get("parent", {}).get("$ref")
                ),
                child_references=[
                    child.get("$ref")
                    for child in element.get("children", [])
                    if child.get("$ref")
                ],
            ),
            metadata=ElementMetadata(
                original_label="table",
                content_layer=element.get("content_layer"),
            ),
            raw_data=element,
        )
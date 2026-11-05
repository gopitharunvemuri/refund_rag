from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

class SourceInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference: str
    collection: str
    page_numbers: list[int] = Field(default_factory=list)
    bounding_boxes: list[dict[str, Any]] = Field(
        default_factory=list
    )

class ElementStructure(BaseModel):
    model_config = ConfigDict(extra="forbid")

    parent_reference: str | None = None
    child_references: list[str] = Field(default_factory=list)
    heading_level: int | None = None
    list_marker: str | None = None
    enumerated: bool | None = None


class ElementMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    original_label: str
    content_layer: str | None = None

class CanonicalElement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0.0"

    element_id: str
    document_id: str

    element_type: Literal[
        "text",
        "section_header",
        "list_item",
        "table",
        "group",
        "picture",
        "other"
    ]

    content: Any = None

    source: SourceInformation
    structure: ElementStructure = Field(
        default_factory=ElementStructure
    )
    metadata: ElementMetadata

    raw_data: dict[str, Any]


sample_element = CanonicalElement(
    element_id="NX-FIN-POL-012-E0001",
    document_id="NX-FIN-POL-012",
    element_type="text",
    content="Employees must submit expense claims within 30 days.",
    source=SourceInformation(
        reference="#/texts/0",
        collection="texts",
        page_numbers=[1],
    ),
    structure=ElementStructure(),
    metadata=ElementMetadata(
        original_label="text",
        content_layer="policy_rule",
    ),
    raw_data={
        "self_ref": "#/texts/0",
        "text": "Employees must submit expense claims within 30 days.",
    },
)

print(sample_element.model_dump_json(indent=2))
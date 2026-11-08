from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


SemanticUnitType = Literal[
    "policy_rule",
    "procedure",
    "approval_rule",
    "spending_limit",
    "exception",
    "definition",
    "condition",
    "table",
    "narrative",
    "cross_reference",
    "unknown",
]

SemanticUnitStatus = Literal[
    "proposed",
    "validated",
    "approved",
    "rejected",
    "review_required",
]


class SemanticUnitSource(BaseModel):
    """References to the canonical elements supporting this semantic unit."""

    model_config = ConfigDict(extra="forbid")

    document_id: str
    element_ids: list[str] = Field(default_factory=list)
    source_references: list[str] = Field(default_factory=list)
    page_numbers: list[int] = Field(default_factory=list)


class SemanticUnitRelationship(BaseModel):
    """A relationship between two semantic units."""

    model_config = ConfigDict(extra="forbid")

    relationship_type: Literal[
        "has_condition",
        "has_exception",
        "requires_approval",
        "overrides",
        "references",
        "belongs_to",
        "depends_on",
        "has_step",
    ]

    target_unit_id: str


class SemanticUnitMetadata(BaseModel):
    """Classification evidence and processing metadata."""

    model_config = ConfigDict(extra="allow")

    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    classification_method: Literal[
        "deterministic",
        "llm",
        "hybrid",
        "human",
    ] = "deterministic"

    review_required: bool = False
    review_reason: str | None = None

    additional_metadata: dict[str, Any] = Field(default_factory=dict)


class SemanticUnit(BaseModel):
    """Normalized semantic unit extracted from canonical document elements."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0.0"

    unit_id: str
    document_id: str

    unit_type: SemanticUnitType
    status: SemanticUnitStatus = "proposed"

    title: str | None = None
    content: str

    source: SemanticUnitSource

    relationships: list[SemanticUnitRelationship] = Field(
        default_factory=list
    )

    metadata: SemanticUnitMetadata = Field(
        default_factory=SemanticUnitMetadata
    )

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ClassificationMethod = Literal[
    "deterministic",
    "llm",
    "hybrid",
    "human",
]

ClassificationReviewStatus = Literal[
    "not_required",
    "pending",
    "approved",
    "rejected",
]


class ClassificationAlternative(BaseModel):
    """An alternative category considered during classification."""

    model_config = ConfigDict(extra="forbid")

    unit_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str


class ClassificationEvidence(BaseModel):
    """Evidence supporting a classification decision."""

    model_config = ConfigDict(extra="forbid")

    evidence_type: Literal[
        "keyword",
        "phrase",
        "pattern",
        "structural_context",
        "element_type",
        "llm_reasoning",
        "human_input",
    ]

    description: str
    source_element_ids: list[str] = Field(default_factory=list)
    matched_text: str | None = None


class ClassificationDecision(BaseModel):
    """Auditable classification decision for a canonical element."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0.0"

    decision_id: str
    document_id: str
    element_id: str

    proposed_unit_type: Literal[
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

    classification_method: ClassificationMethod

    confidence: float = Field(ge=0.0, le=1.0)

    evidence: list[ClassificationEvidence] = Field(
        default_factory=list
    )

    matched_rule_ids: list[str] = Field(default_factory=list)

    alternatives: list[ClassificationAlternative] = Field(
        default_factory=list
    )

    review_status: ClassificationReviewStatus = "not_required"

    review_reason: str | None = None

    classifier_version: str

    configuration_version: str

    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_review_status(self):
        """Ensure review decisions have an explanatory reason."""

        if self.review_status == "pending" and not self.review_reason:
            raise ValueError(
                "A review reason is required when review_status is pending"
            )

        return self

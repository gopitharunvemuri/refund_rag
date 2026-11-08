from enum import Enum


class SemanticUnitType(str, Enum):
    POLICY_RULE = "policy_rule"
    PROCEDURE = "procedure"
    APPROVAL_RULE = "approval_rule"
    SPENDING_LIMIT = "spending_limit"
    EXCEPTION = "exception"
    DEFINITION = "definition"
    CONDITION = "condition"
    TABLE = "table"
    NARRATIVE = "narrative"
    CROSS_REFERENCE = "cross_reference"
    UNKNOWN = "unknown"


class SemanticRelationshipType(str, Enum):
    HAS_CONDITION = "has_condition"
    HAS_EXCEPTION = "has_exception"
    REQUIRES_APPROVAL = "requires_approval"
    OVERRIDES = "overrides"
    REFERENCES = "references"
    BELONGS_TO = "belongs_to"
    DEPENDS_ON = "depends_on"
    HAS_STEP = "has_step"


class SemanticUnitStatus(str, Enum):
    PROPOSED = "proposed"
    VALIDATED = "validated"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"


SEMANTIC_UNIT_TYPES = [item.value for item in SemanticUnitType]

SEMANTIC_RELATIONSHIP_TYPES = [
    item.value for item in SemanticRelationshipType
]

SEMANTIC_UNIT_STATUSES = [
    item.value for item in SemanticUnitStatus
]
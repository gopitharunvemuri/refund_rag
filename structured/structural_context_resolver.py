
from typing import Any

from structured.canonical_representation import CanonicalElement


class StructuralContextResolver:
    """Resolves canonical elements and document structural containers."""

    def __init__(
        self,
        elements: list[CanonicalElement],
        structural_nodes: dict[str, dict[str, Any]] | None = None,
    ):
        self.elements = elements
        self.structural_nodes = structural_nodes or {}

        self.element_index: dict[str, CanonicalElement] = {}
        self.reference_index: dict[str, CanonicalElement] = {}

        self.audit_errors: list[dict[str, Any]] = []
        self._recorded_errors: set[tuple] = set()

        self._build_index()

    def _record_error(self, error: dict[str, Any]) -> None:
        """Record each unique structural error only once."""

        error_key = tuple(sorted(error.items()))

        if error_key not in self._recorded_errors:
            self._recorded_errors.add(error_key)
            self.audit_errors.append(error)

    def _build_index(self) -> None:
        """Build indexes for canonical elements."""

        for element in self.elements:

            if element.element_id in self.element_index:
                self._record_error({
                    "error": "duplicate_element_id",
                    "element_id": element.element_id,
                })
                continue

            self.element_index[element.element_id] = element

            reference = element.source.reference

            if reference in self.reference_index:
                self._record_error({
                    "error": "duplicate_source_reference",
                    "reference": reference,
                })
                continue

            self.reference_index[reference] = element

    def _resolve_parent_reference(
        self,
        reference: str,
    ) -> CanonicalElement | dict[str, Any] | None:
        """Resolve a canonical element or structural container."""

        element = self.reference_index.get(reference)

        if element is not None:
            return element

        structural_node = self.structural_nodes.get(reference)

        if structural_node is not None:
            return structural_node

        return None

    def get_parent(
        self,
        element: CanonicalElement,
    ) -> CanonicalElement | None:
        """Return the canonical parent when one exists."""

        parent_reference = element.structure.parent_reference

        if not parent_reference:
            return None

        parent = self.reference_index.get(parent_reference)

        if parent is not None:
            return parent

        if parent_reference in self.structural_nodes:
            return None

        self._record_error({
            "error": "parent_reference_not_found",
            "element_id": element.element_id,
            "parent_reference": parent_reference,
        })

        return None

    def get_children(
        self,
        element: CanonicalElement,
    ) -> list[CanonicalElement]:
        """Return canonical children in their declared order."""

        children = []

        for child_reference in element.structure.child_references:

            child = self.reference_index.get(child_reference)

            if child is not None:
                children.append(child)

            elif child_reference not in self.structural_nodes:
                self._record_error({
                    "error": "child_reference_not_found",
                    "element_id": element.element_id,
                    "child_reference": child_reference,
                })

        return children

    def get_nearest_section_heading(
        self,
        element: CanonicalElement,
    ) -> CanonicalElement | None:
        """Find the nearest section heading in the parent hierarchy."""

        current_element = element
        visited = set()

        while current_element is not None:

            if current_element.element_type == "section_header":
                return current_element

            if current_element.element_id in visited:
                self._record_error({
                    "error": "parent_relationship_cycle",
                    "element_id": current_element.element_id,
                })
                return None

            visited.add(current_element.element_id)

            parent_reference = current_element.structure.parent_reference

            if not parent_reference:
                return None

            parent = self._resolve_parent_reference(parent_reference)

            if parent is None:
                self._record_error({
                    "error": "parent_reference_not_found",
                    "element_id": current_element.element_id,
                    "parent_reference": parent_reference,
                })
                return None

            if isinstance(parent, dict):
                return None

            current_element = parent

        return None

    def get_structural_context(
        self,
        element: CanonicalElement,
    ) -> dict[str, Any]:
        """Return structural context for one canonical element."""

        if element.element_id not in self.element_index:
            raise ValueError(
                f"Element not found in resolver index: {element.element_id}"
            )

        parent = self.get_parent(element)
        children = self.get_children(element)
        heading = self.get_nearest_section_heading(element)

        parent_reference = element.structure.parent_reference

        return {
            "element_id": element.element_id,
            "document_id": element.document_id,
            "element_type": element.element_type,
            "content": element.content,

            "parent": (
                {
                    "element_id": parent.element_id,
                    "element_type": parent.element_type,
                    "content": parent.content,
                }
                if parent else None
            ),

            "parent_reference": parent_reference,

            "parent_is_structural_container": (
                parent_reference in self.structural_nodes
                if parent_reference else False
            ),

            "children": [
                {
                    "element_id": child.element_id,
                    "element_type": child.element_type,
                    "content": child.content,
                }
                for child in children
            ],

            "nearest_section_heading": (
                {
                    "element_id": heading.element_id,
                    "content": heading.content,
                    "heading_level": heading.structure.heading_level,
                }
                if heading else None
            ),

            "page_numbers": element.source.page_numbers,
        }

    def get_audit_errors(self) -> list[dict[str, Any]]:
        """Return structural resolution errors."""

        return list(self.audit_errors)

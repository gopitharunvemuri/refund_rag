
from pathlib import Path

from structured.docling_reader import DoclingReader
from structured.reference_resolver import ReferenceResolver
from structured.element_mapper import ElementMapper
from structured.structural_context_resolver import (
    StructuralContextResolver,
)


PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DOCUMENTS_DIR = PROJECT_DIR / "parsed_documents" / "raw"

DOCUMENT_IDS = [
    "NX-FIN-POL-012",
    "NX-FIN-POL-013",
    "NX-FIN-POL-014",
]


def load_canonical_elements(document_id: str):
    """Load one Docling document and map its elements."""

    reader = DoclingReader(RAW_DOCUMENTS_DIR)

    document = reader.read_document(document_id)

    reference_resolver = ReferenceResolver(
        document,
        document_id=document_id,
    )

    mapper = ElementMapper(document_id)

    canonical_elements = []

    for collection_name in [
        "texts",
        "tables",
        "groups",
        "list_items",
    ]:

        elements = document.get(collection_name, [])

        for element in elements:

            label = element.get("label")

            if collection_name == "groups":

                canonical_elements.append(
                    mapper.map_group(element)
                )

            elif label in ["text", "section_header", "page_footer"]:

                canonical_elements.append(
                    mapper.map_text_element(element)
                )

            elif label == "list_item":

                canonical_elements.append(
                    mapper.map_list_item(element)
                )

            elif label == "table":

                canonical_elements.append(
                    mapper.map_table(element)
                )

    return canonical_elements, reference_resolver, document


def test_structural_context_resolver():

    total_elements = 0
    total_contexts = 0

    for document_id in DOCUMENT_IDS:

        print(f"\nTesting document: {document_id}")

        (
            canonical_elements,
            reference_resolver,
            document,
        ) = load_canonical_elements(document_id)

        # Preserve the original Docling body as a structural container.
        body = document.get("body", {})

        structural_nodes = {}

        if isinstance(body, dict) and body.get("self_ref"):

            structural_nodes[body["self_ref"]] = body

        # Initialize the structural context resolver.
        resolver = StructuralContextResolver(
            canonical_elements,
            structural_nodes=structural_nodes,
        )

        # Validate canonical element indexing.
        assert len(resolver.element_index) == len(canonical_elements)

        assert len(resolver.reference_index) == len(canonical_elements)

        # Validate original Docling source references.
        for element in canonical_elements:

            validation = reference_resolver.validate_reference(
                element.source.reference
            )

            assert validation["valid"], (
                f"Invalid source reference: {element.source.reference}"
            )

        # Validate the structural body reference.
        if isinstance(body, dict) and body.get("self_ref"):

            assert body["self_ref"] in resolver.structural_nodes

        # Generate structural context for every canonical element.
        for element in canonical_elements:

            context = resolver.get_structural_context(element)

            assert context["element_id"] == element.element_id

            assert context["document_id"] == document_id

            assert "parent" in context

            assert "parent_reference" in context

            assert "parent_is_structural_container" in context

            assert "children" in context

            assert "nearest_section_heading" in context

            assert "page_numbers" in context

            total_contexts += 1

        total_elements += len(canonical_elements)

        print("Canonical elements:", len(canonical_elements))

        print("Element index entries:", len(resolver.element_index))

        print("Reference index entries:", len(resolver.reference_index))

        print("Structural nodes:", len(resolver.structural_nodes))

        print("Structural contexts generated:", len(canonical_elements))

        print("Structural audit errors:", len(resolver.get_audit_errors()))

        print("\nFirst 10 structural audit errors:")

        for error in resolver.get_audit_errors()[:10]:

            print(error)

    print("\nSTRUCTURAL CONTEXT RESOLVER TEST SUMMARY")
    print("----------------------------------------")

    print("Total canonical elements:", total_elements)

    print("Total structural contexts:", total_contexts)

    assert total_elements == 559

    assert total_contexts == 559

    print("\nSTRUCTURAL CONTEXT RESOLVER TEST PASSED")


if __name__ == "__main__":

    test_structural_context_resolver()

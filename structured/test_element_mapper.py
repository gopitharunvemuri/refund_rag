
from pathlib import Path

from structured.docling_reader import DoclingReader
from structured.element_mapper import ElementMapper


DOCUMENT_IDS = [
    "NX-FIN-POL-012",
    "NX-FIN-POL-013",
    "NX-FIN-POL-014",
]

reader = DoclingReader(Path("parsed_documents/raw"))

all_mapped_elements = []

for document_id in DOCUMENT_IDS:
    document = reader.read_document(document_id)
    mapper = ElementMapper(document_id)

    mapped_elements = []

    # Map text, section headers, and page footers
    for element in document.get("texts", []):
        label = element.get("label")

        if label in ("text", "section_header", "page_footer"):
            mapped_elements.append(
                mapper.map_text_element(element)
            )

        elif label == "list_item":
            mapped_elements.append(
                mapper.map_list_item(element)
            )

    # Map tables
    for table in document.get("tables", []):
        mapped_elements.append(
            mapper.map_table(table)
        )

    # Map groups
    for group in document.get("groups", []):
        mapped_elements.append(
            mapper.map_group(group)
        )

    all_mapped_elements.extend(mapped_elements)

    print(f"\n{document_id}")
    print(f"Total mapped elements: {len(mapped_elements)}")


# Validate total element count

expected_total = 559
actual_total = len(all_mapped_elements)

print("\nTOTAL ELEMENT COUNT")
print(f"Expected: {expected_total}")
print(f"Actual:   {actual_total}")

assert actual_total == expected_total, (
    f"Expected {expected_total} elements, got {actual_total}"
)


# Validate unique element IDs

element_ids = [
    element.element_id
    for element in all_mapped_elements
]

unique_element_ids = set(element_ids)

print("\nELEMENT ID VALIDATION")
print(f"Total IDs:  {len(element_ids)}")
print(f"Unique IDs: {len(unique_element_ids)}")

assert len(element_ids) == len(unique_element_ids), (
    "Duplicate element IDs found"
)


# Validate unique source references


# Validate unique source references within each document

references = [
    (element.document_id, element.source.reference)
    for element in all_mapped_elements
]

unique_references = set(references)

print("\nSOURCE REFERENCE VALIDATION")
print(f"Total references:  {len(references)}")
print(f"Unique references: {len(unique_references)}")

assert len(references) == len(unique_references), (
    "Duplicate source references found within a document"
)



# Validate document IDs

invalid_document_ids = [
    element
    for element in all_mapped_elements
    if element.document_id not in DOCUMENT_IDS
]

print("\nDOCUMENT ID VALIDATION")
print(f"Invalid document IDs: {len(invalid_document_ids)}")

assert not invalid_document_ids, (
    "Elements with invalid document IDs found"
)


# Validate element IDs match their document IDs

invalid_element_ids = [
    element
    for element in all_mapped_elements
    if not element.element_id.startswith(
        f"{element.document_id}-"
    )
]

print("\nELEMENT ID PREFIX VALIDATION")
print(f"Invalid ID prefixes: {len(invalid_element_ids)}")

assert not invalid_element_ids, (
    "Element IDs do not match their document IDs"
)


# Final result

print("\n" + "=" * 45)
print("CANONICAL ELEMENT MAPPING VALIDATION PASSED")
print("=" * 45)
print(f"Total canonical elements: {actual_total}")
print(f"Unique element IDs:      {len(unique_element_ids)}")
print(f"Unique source references: {len(unique_references)}")
print("All document IDs are valid.")
print("All canonical elements passed Pydantic validation.")

from pathlib import Path

from structured.docling_reader import DoclingReader
from structured.element_mapper import ElementMapper


document = DoclingReader(
    Path("parsed_documents/raw")
).read_document("NX-FIN-POL-012")

mapper = ElementMapper("NX-FIN-POL-012")

text_element = document["texts"][0]

section_header = next(
    element
    for element in document["texts"]
    if element.get("label") == "section_header"
)

mapped_text = mapper.map_text_element(text_element)
mapped_header = mapper.map_text_element(section_header)

# print("TEXT ELEMENT:")
# print(mapped_text.model_dump_json(indent=2))

# print("\nSECTION HEADER:")
# print(mapped_header.model_dump_json(indent=2))
list_item = next(
    element
    for element in document["texts"]
    if element.get("label") == "list_item"
)

mapped_list_item = mapper.map_list_item(list_item)

# print("\nLIST ITEM:")
# print(mapped_list_item.model_dump_json(indent=2))

# group = document["groups"][0]

# mapped_group = mapper.map_group(group)

# print("\nGROUP:")
# print(mapped_group.model_dump_json(indent=2))
# first_table = document["tables"][0]
# mapped_table = mapper.map_table(first_table)

# print("\nMAPPED TABLE")
# print(mapped_table.model_dump_json(indent=2))

footer = next(
    item
    for item in document["texts"]
    if item.get("label") == "page_footer"
)

mapped_footer = mapper.map_text_element(footer)

print("\nMAPPED PAGE FOOTER")
print(mapped_footer.model_dump_json(indent=2))


# Test all text elements across all three documents

from collections import Counter

# for document_id in [
#     "NX-FIN-POL-012",
#     "NX-FIN-POL-013",
#     "NX-FIN-POL-014",
# ]:
#     document = DoclingReader(
#         Path("parsed_documents/raw")
#     ).read_document(document_id)

#     mapper = ElementMapper(document_id)

#     mapped_elements = [
#         mapper.map_text_element(element)
#         for element in document["texts"]
#         if element.get("label") in (
#             "text",
#             "section_header",
#             "page_footer",
#         )
#     ]

#     print(f"\n{document_id}")
#     print(f"Total mapped: {len(mapped_elements)}")
#     print(
#         "Element types:",
#         Counter(element.element_type for element in mapped_elements),
#     )

# Test all list items across all three documents

# for document_id in [
#     "NX-FIN-POL-012",
#     "NX-FIN-POL-013",
#     "NX-FIN-POL-014",
# ]:
#     document = DoclingReader(
#         Path("parsed_documents/raw")
#     ).read_document(document_id)

#     mapper = ElementMapper(document_id)

#     list_items = [
#         element
#         for element in document["texts"]
#         if element.get("label") == "list_item"
#     ]

#     mapped_list_items = [
#         mapper.map_list_item(element)
#         for element in list_items
#     ]

#     print(f"\n{document_id}")
#     print(f"List items found: {len(list_items)}")
#     print(f"List items mapped: {len(mapped_list_items)}")


# Test all tables across all three documents

# for document_id in [
#     "NX-FIN-POL-012",
#     "NX-FIN-POL-013",
#     "NX-FIN-POL-014",
# ]:
#     document = DoclingReader(
#         Path("parsed_documents/raw")
#     ).read_document(document_id)

#     mapper = ElementMapper(document_id)

#     tables = document.get("tables", [])

#     mapped_tables = [
#         mapper.map_table(table)
#         for table in tables
#     ]

#     print(f"\n{document_id}")
#     print(f"Tables found: {len(tables)}")
#     print(f"Tables mapped: {len(mapped_tables)}")


# Test all groups across all three documents

for document_id in [
    "NX-FIN-POL-012",
    "NX-FIN-POL-013",
    "NX-FIN-POL-014",
]:
    document = DoclingReader(
        Path("parsed_documents/raw")
    ).read_document(document_id)

    mapper = ElementMapper(document_id)

    groups = document.get("groups", [])

    mapped_groups = [
        mapper.map_group(group)
        for group in groups
    ]

    print(f"\n{document_id}")
    print(f"Groups found: {len(groups)}")
    print(f"Groups mapped: {len(mapped_groups)}")
import re
import streamlit as st


def build_checklist(section_title, items, separator=None):
    print(f"\n--- Section: {section_title} ---")
    print(f"\n--- Separator: {separator} ---")
    # print("Raw items:", items)

    st.markdown(f"**{section_title}**")
    selected = []
    checkbox_counter = 0

    parsed_items = parse_items(items, separator)

    for item in parsed_items:
        unique_key = f"{section_title}_{item}_{checkbox_counter}"
        if st.checkbox(item, key=unique_key):
            selected.append(item)
        checkbox_counter += 1

    return selected


def parse_items(items, separator=None):
    """
    Parses and flattens a list of strings by splitting on the given separator,
    while ignoring empty or whitespace-only items but preserving valid spacing.
    """
    
    if not items:
        return []
    
        # Join all items into a single string
    combined = "".join(item for item in items if (stripped := item) and stripped.strip() != "")
    print(f"Combined items: {combined}")



    if separator:
        split_pattern = re.escape(separator)
        # Removes a whitespace from the beginning and end of the separator
        sub_items = re.split(fr"\s*{split_pattern}\s*", combined)
        return [item for item in sub_items if item]
    else:
        return [combined]

    
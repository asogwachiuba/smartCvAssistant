import streamlit as st
from cv_parser import extract_cv_sections
from content_selector import build_checklist
from pdf_generator import generate_pdf

st.title("🧠 Resume Reader")

uploaded_file = st.file_uploader("Upload your CV (.docx)", type="docx")

# 1. Section style input UI
st.subheader("⚙️ Define Section Title")

# Allow user to define multiple rules
section_style_config = []

counter = 0

# Use a number input to control how many rules the user wants to add
num_rules = st.number_input("How many section are in your Resume?", min_value=1, max_value=10, value=3)

for i in range(num_rules):
    with st.expander(f"Section Title Description {i+1}"):
        section_title = st.text_input(f"Section Title {i+1}", key=f"title_{i}")
        font_size = st.number_input(f"Minimum Font Size for '{section_title}' (optional)", min_value=1, max_value=100, value=1, key=f"size_{i}")
        is_bold = st.checkbox(f"Bold?", value=True, key=f"bold_{i}")
        is_italic = st.checkbox(f"Italic?", value=False, key=f"italic_{i}")
        
        separator_option = st.selectbox(
            f"Choose a separator for items/points under '{section_title}'",
            options=["None", ", (comma)", "| (pipe)", "; (semicolon)", "\\n (new line)", "Other..."],
            key=f"separator_option_{i}"
        )

        if separator_option == "Other...":
            custom_separator = st.text_input("Enter your custom separator", key=f"custom_sep_{i}")
        elif separator_option == "None":
            custom_separator = None  # Explicitly use None when no separator is desired
        elif separator_option.startswith("\\n"):
            custom_separator = "\n"  # Convert readable form to actual newline character
        else:
            custom_separator = separator_option.split()[0]  # Extract the actual symbol


        # ✅ Add the duplicate check here
        if section_title:
            title_lower = section_title.strip().lower()
            existing_titles = [rule["title"].strip().lower() for rule in section_style_config]
            if title_lower in existing_titles:
                st.error(f"❌ A style rule for '{section_title}' already exists. Please use a different name.")
            else:
                section_style_config.append({
                    "title": section_title,
                    "font_size": font_size,
                    "bold": is_bold,
                    "italic": is_italic,
                    "separator": custom_separator
                })
        
        

# Now process the uploaded file
if uploaded_file:
    print("\n==== Uploaded File ====" + counter.__str__())
    counter += 1
    # 2. Pass section style config to the extractor
    sections = extract_cv_sections(uploaded_file, section_style_config)
    
    # print("\n==== Extracted Sections ====")
    # if not sections:
    #     print("⚠️ No sections were detected. Check your rules or formatting.")
    for title, items in sections.items():
        print(f"\n--- {title} ---")
    #     for item in items:
    #         print(f"- {item}")


    st.subheader("🎯 All Section contents are Available")
    selected_content = {}

    for section, items in sections.items():
        # Find matching rule
        matching_rule = next((rule for rule in section_style_config if rule["title"] == section), None)
        separator = matching_rule.get("separator", None) if matching_rule else None
        selected_content[section] = build_checklist(section, items, separator)

    # 3. PDF generation button
    # if st.button("✅ Generate Custom CV"):
    #     output_path = generate_pdf(selected_content)
    #     with open(output_path, "rb") as f:
    #         st.download_button("📄 Download Custom CV", f, file_name="custom_cv.pdf")

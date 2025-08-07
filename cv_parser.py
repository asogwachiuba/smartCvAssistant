from docx import Document

def extract_cv_sections(docx_file, style_config):
    document = Document(docx_file)
    sections = {}
    current_section = None

    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Get font size
        font_sizes = [run.font.size.pt for run in para.runs if run.font.size]
        max_font_size = max(font_sizes) if font_sizes else None

        # print(f"\nAnalyzing paragraph: '{text}' | Size: {max_font_size}")

        matched = False
        for rule in style_config:
            matches_title = text.lower().startswith(rule["title"].lower()) 
            matches_bold = False
            matches_italic = False
            matches_font = False
            if(matches_title):
                matches_bold = rule["bold"] == is_title_bold_in_runs(para.runs, rule["title"], para.style)
                matches_italic = True if rule["italic"] == False else any(run.italic for run in para.runs)
                matches_font = max_font_size >= rule["font_size"] if rule["font_size"] and max_font_size else True

            # print(f"Checking rule: {rule['title']} | Matches Title: {matches_title}, Bold: {matches_bold}, Italic: {matches_italic}, Font Size: {matches_font}")
            if matches_title and matches_bold and matches_italic and matches_font:
                matched = True

                # Extract title and rest of the line (if any)
                full_text = text.strip()
                rule_title = rule["title"].strip()
                current_section = rule_title
                remaining = full_text[len(rule_title):].strip()  # cut off the matched title

                # Initialize section and optionally include remaining content
                sections[current_section] = []
                if remaining:
                    sections[current_section].append(remaining)
                break


        if not matched and current_section:
            sections[current_section].append(text)
                
    # print("\n--- Sections extracted ---")
    # for title, items in sections.items():
    #     print(f"\n--- {title} ---")
    #     for item in items:
    #         print(f"- {item}")
    return sections


def is_title_bold_in_runs(runs, title, paragraph_style=None):
    title = title.strip().lower()
    buffer = ""
    bold_buffer = ""

    # Determine if the paragraph style applies bold by default
    style_is_bold = False
    if paragraph_style and paragraph_style.font:
        style_is_bold = paragraph_style.font.bold is True


    for run in runs:
        run_text = run.text
        # Check if the run is explicitly bold or inherits from paragraph style
        is_bold = run.bold is True or (run.bold is None and style_is_bold)

        buffer += run_text
        if is_bold:
            bold_buffer += run_text


        if len(buffer) >= len(title):
            break

    return title in bold_buffer.lower()


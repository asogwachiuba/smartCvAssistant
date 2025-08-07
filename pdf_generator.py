from docxtpl import DocxTemplate
import pdfkit
import os

def generate_pdf(selected_sections):
    doc = DocxTemplate("cv_template.docx")
    context = {k.upper(): v for k, v in selected_sections.items()}
    context["name"] = "Chi-Uba Asogwa"
    context["email"] = "ishiuba488@gmail.com"

    doc.render(context)
    doc_path = "generated_cv.docx"
    pdf_path = "custom_cv.pdf"
    
    doc.save(doc_path)
    os.system(f"libreoffice --headless --convert-to pdf {doc_path} --outdir .")
    return pdf_path

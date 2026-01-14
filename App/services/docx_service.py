from docx import Document

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs]
    return ".\n".join(full_text)
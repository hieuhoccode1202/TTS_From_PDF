import pdfplumber
from App.services.ocr_service import run_paddle_ocr
import re


def extract_text_without_page_numbers(page):
    width = page.width
    height = page.height

    safe_zone = (0, height * 0.05, width, height * 0.95)
    
    content = page.within_bbox(safe_zone).extract_text()
    return content if content else ""



def clean_page_numbers(text):
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(Trang|Page)\s*\d+', '', text, flags=re.IGNORECASE)

    text = re.sub(r'\d+\s*/\s*\d+', '', text)
    
    text = re.sub(r'\n\s*\n', '\n', text) 
    return text.strip()


def extract_text_from_pdf(file_path : str, threshold : int = 50):
    text_content = ""
    #get text from pdf file
    with pdfplumber.open(file_path) as pdf:
        num_page = len(pdf.pages)
        if num_page == 0:
            return run_paddle_ocr(file_path=file_path)
        
        for page in pdf.pages:
            page_text = extract_text_without_page_numbers(page=page)
            if page_text:
                text_content += page_text + "\n"
    clean_text = clean_page_numbers(text=text_content)
    #checking
    num_text = len(text_content)
    avg_char = num_text / num_page

    if (avg_char > threshold):
        return clean_text
    
    return run_paddle_ocr(file_path=file_path)

from App.services.ocr_model import HybridOCR
import os

def run_paddle_ocr(file_path):

    ocr = HybridOCR()
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]:
        return ocr.process_image(file_path)
    if ext == ".pdf":
        return ocr.process_pdf(file_path)
    
    raise ValueError("Định dạng file không được hỗ trợ")

import os
from App.services import docx_service, pdf_service, ocr_service, tts_service
import glob

class Main_service:
    def __init__(self):
        self.input_dir = "./storage/uploads"
        self.output_dir = "./storage/outputs/test.mp3"
        self.tts = tts_service.TTS()
    def run(self):
       
        for file_path in os.listdir(self.input_dir):
            ext = os.path.splitext(file_path)[1].lower()
            path = os.path.join(self.input_dir, file_path)
            text = "k"
            if ext in ['.docx', '.doc']:
                text =  docx_service.extract_text_from_docx(file_path=path)
            elif ext == '.pdf':
                text = pdf_service.extract_text_from_pdf(file_path=path)
            elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]:
                text = ocr_service.run_paddle_ocr(file_path=path)
                print("hihi")
            print(text)
            self.tts.convert_text_to_mp3(text= text, output_path=self.output_dir)
test = Main_service()
test.run()
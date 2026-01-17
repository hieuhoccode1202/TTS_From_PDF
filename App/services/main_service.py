import os
import asyncio
from App.services import docx_service, pdf_service, ocr_service, tts_service, smooth_text

class Main_service:
    def __init__(self):
        self.input_dir = "./storage/uploads"
        self.output_dir = "./storage/outputs"
        self.tts = tts_service.TTS()
        self.llm = smooth_text.LLMService()

    async def run_async(self, file_path):
        """Hàm xử lý chính dạng async"""
        if not os.path.exists(self.input_dir):
            return

        files = os.listdir(self.input_dir)
        for file_name in files:
            path = file_path
            ext = os.path.splitext(file_path)[1].lower()
            text = ""

            # 1. OCR (Đồng bộ)
            if ext in ['.docx', '.doc']:
                text = docx_service.extract_text_from_docx(path)
            elif ext == '.pdf':
                text = pdf_service.extract_text_from_pdf(path)
            elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
                text = ocr_service.run_paddle_ocr(path)

            if text and text.strip():
                # 2. Làm mượt với Gemini (AWAIT)
                print(f"--- Đang làm mượt: {file_path} ---")
                refined_text = await self.llm.smooth_text(text)
                # print(refined_text)
                # 3. Chuyển TTS (AWAIT)
                base_name = os.path.splitext(file_name)[0]
                mp3_path = os.path.join(self.output_dir, f"{base_name}.mp3")
                
                print(f"--- Đang tạo voice cho: {base_name} ---")
                await self.tts.convert_text_to_mp3(refined_text, mp3_path)
                return mp3_path
            return None
import os
import google.generativeai as genai
import asyncio
from dotenv import load_dotenv

# Load môi trường
load_dotenv()

class LLMService:
    def __init__(self):
        # Đảm bảo tên biến trong .env khớp với os.getenv
        api_key = os.getenv("API_KEY") 
        if not api_key:
            raise ValueError("Không tìm thấy API_KEY trong file .env")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def smooth_text(self, raw_text):
        if not raw_text or not raw_text.strip():
            return ""

        prompt = f"""
                Nhiệm vụ: Chỉnh sửa văn bản OCR thô sau đây thành văn bản tiếng Việt mượt mà.
                - Nối các dòng bị ngắt quãng.
                - Sửa lỗi chính tả.
                - Giữ nguyên ý nghĩa.
                - Trả về kết quả duy nhất là đoạn văn đã sửa.
                - Xóa bỏ hết các markdown.
                - Nối các câu thành các đoạn văn hoàn chỉnh.
                Văn bản thô:
                {raw_text}
                """
        
        try:
            # Gọi API
            response = await self.model.generate_content_async(prompt)
            print(response)
            return response.text.strip()
        except Exception as e:
            return f"[Gemini Error] {e}"

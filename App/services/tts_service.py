import edge_tts
import os

class TTS:
    def __init__(self):
        self.voice = "vi-VN-HoaiMyNeural"

    async def convert_text_to_mp3(self, text, output_path):
        """Hàm này bây giờ là async và không dùng asyncio.run() bên trong nữa"""
        try:
            clean_text = text.replace('\n', ' ')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            communicate = edge_tts.Communicate(clean_text, self.voice, rate="-10%")
            await communicate.save(output_path)
            
            print(f"[Edge-TTS] Thành công: {output_path}")
            return True
        except Exception as e:
            print(f"[Edge-TTS Error] {e}")
            return False
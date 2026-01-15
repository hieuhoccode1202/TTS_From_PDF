from gtts import gTTS
import os

class TTS:
    def __init__(self):
        self.lang = 'vi'

    def convert_text_to_mp3(self, text, output_path):

        try:
            if os.path.isdir(output_path):
                print(f"[TTS Error] output_path đang là thư mục, cần có tên file cụ thể!")
                return False

            dir_name = os.path.dirname(output_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            clean_text = text.replace('\n', ' ')
            tts = gTTS(text=clean_text, lang=self.lang, slow=False)
            tts.save(output_path)
            print(f"[TTS] Thành công: {output_path}")
            return True
        
        except Exception as e:
            print(f"[TTS Error] {e}")
            return False

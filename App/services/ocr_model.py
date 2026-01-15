import cv2
import numpy as np
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR
from App.conf import DEVICE, REC_MODEL
from pdf2image import convert_from_path
class HybridOCR:
    def __init__(self):
        self.detector = PaddleOCR(use_angle_cls=False, lang='en', det=True, rec=False, show_log=False)

        config = Cfg.load_config_from_name(REC_MODEL)
        config['device'] = DEVICE
        self.recognizer = Predictor(config)

    def process_image(self, img_path):
        result = self.detector.ocr(img_path, cls=False)
        
        if result is None or result[0] is None:
            print("Không tìm thấy chữ nào!")
            return []

        boxes = result[0]
        original_img = cv2.imread(img_path)
        final_results = ""

        for item in boxes:
            if isinstance(item[0], list) and len(item) == 2 and isinstance(item[1], tuple):
                 box = item[0]
            else:
                 box = item
            
            points = np.array(box, dtype=np.int32)

            x, y, w, h = cv2.boundingRect(points)
            
            pad = 5 
            h_img, w_img, _ = original_img.shape
            
            crop_img = original_img[
                max(0, y-pad):min(h_img, y+h+pad), 
                max(0, x-pad):min(w_img, x+w+pad)
            ]

            try:
                crop_img_pil = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
                text = self.recognizer.predict(crop_img_pil)
                final_results += text + "\n"
            except Exception as e:
                print(f"Lỗi box: {e}")
                continue

        return final_results

    def process_pdf(self, pdf_path):
  
        pages = convert_from_path(pdf_path, dpi=300) 
        
        full_document_text = ""

        for i, page in enumerate(pages):

            open_cv_image = np.array(page)
            open_cv_image = open_cv_image[:, :, ::-1].copy() 

            page_text = self._ocr_logic(open_cv_image)
            full_document_text += page_text + "\n"
        return full_document_text
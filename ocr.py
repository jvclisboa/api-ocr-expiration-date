from paddleocr import PaddleOCR,draw_ocr
import os 
from datetime import datetime
import dateutil.parser
import re

# Essa linha de código foi necessária pra rodar o OCR. Tava dando um erro e ela resolveu.
os.environ['KMP_DUPLICATE_LIB_OK']='True'

def read_image(img_path):
    ocr = PaddleOCR(lang='latin')
    result = ocr.ocr(img_path)
    
    try:
        
        for line in result:
            m = re.search(r'[0-9]{1,2}(/|-|\.)?[0-9]{1,2}(/|-|\.)[0-9]{2,4}', line[1][0])
        
            if m:
                date = datetime.min
                date_str = m.group()
                date_time = dateutil.parser.parse(date_str , default= datetime(2021, 1, 1, 0, 0), dayfirst=True)        
                if date_time > date:
                    date = date_time
        date_formatted = date.strftime('%d/%m/%Y')
        return 'A data de validade do produto é {}'.format(date_formatted)
    except:
        return 'Não foi possível encontrar a data de validade'
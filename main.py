from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#import ocr
import os
import shutil
from paddleocr import PaddleOCR,draw_ocr
import os 
from datetime import datetime
import dateutil.parser
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/postocr")
async def post_ocr(image: UploadFile = File(...)):
    temp_file = _save_file_to_disk(image, path="temp", save_as="temp")
    text = read_image(temp_file)
    return {"filename": image.filename, "text": text}

def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file

os.environ['KMP_DUPLICATE_LIB_OK']='True'
ocr = PaddleOCR(lang='latin')

def read_image(img_path):
    
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
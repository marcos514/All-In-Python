
# If you need any other supported languages, run `brew install tesseract-lang`.
import csv
from io import StringIO
from numpy import Infinity
import numpy as np
import pandas as pd
import cv2
import pytesseract
from urllib.request import Request, urlopen

from ..types import ImageLineTextData, ImageTextPosition

def url_to_image(img_url:str, is_online=True):
    image = None
    if is_online:
        hdr = {
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
        }
        img_request = Request(
            url=img_url, 
            headers=hdr,                
        )
        resp = urlopen(img_request)
        np_img = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(np_img, -1)
    else:
        image = cv2.imread(img_url)
    return image


def image_to_df_text_data(img, lang='eng', config: str='') -> pd.DataFrame:
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # hImg, wImg, _ = img.shape
    # config='--psm 6'
    # --psm 6 tsv  digits
    boxes = pytesseract.image_to_data(img, lang, config=config)

    StringData = StringIO(boxes)
    df = pd.read_csv(StringData, sep ="\t", quoting=csv.QUOTE_NONE, encoding='utf-8')
    return df.to_dict(orient='records')


def get_text_positions(df) -> ImageTextPosition:
    sentences_places = { }
    for row in df:
        conf = row['conf']
        block_num = row['block_num']
        line_num = row['line_num']
        x = row['left']
        y = row['top']
        w = row['width']
        h = row['height']
        text = row.get('text', '')
        if text and conf >= 0:
            if block_num not in sentences_places:
                sentences_places[block_num] = ImageTextPosition(full_text='', all_sentences={})

            block = sentences_places[block_num]
            if line_num not in block.all_sentences:
                block.all_sentences[line_num] = ImageLineTextData(
                    x_first=Infinity, y_first=Infinity, x_last=0, y_last=0, width=0, height=0, text=''
                )

            line = block.all_sentences[line_num]

            # Update the attributes based on the new row data
            line.x_first = min(line.x_first, x)
            line.y_first = min(line.y_first, y)
            line.x_last = max(line.x_last, x)
            line.width = max(line.width, w)
            line.y_last = max(line.y_last, y)
            line.height = max(line.height, h)

            # Update text
            line.text += f" {text}"
            block.full_text += f" {text}"
    return sentences_places

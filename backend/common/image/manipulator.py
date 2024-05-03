# If you need any other supported languages, run `brew install tesseract-lang`.
import cv2
import base64

from ..types import Translators, ImageTextPosition
from ..utils import translate_text_factory

def img_to_base64(img, extension='.jpg'):
    _, im_arr = cv2.imencode(extension, img)  # im_arr: image in Numpy one-dim array format.
    im_b64 = base64.b64encode(im_arr)
    return im_b64.decode('utf-8')


def translate_text_boxes(img: cv2.typing.MatLike, sentences_places: ImageTextPosition, source= 'auto', target= 'english'):
    for _, sentence in sentences_places.items():
        full_text: str = sentence.full_text.strip()
        all_worlds = full_text.split(' ')
        translated_text = translate_text_factory(Translators.GOOGLE, full_text, source, target)
        if not translated_text:
            continue

        translated_text = translated_text.strip()
        translated_worlds = translated_text.strip().split(' ')
        for _, worlds in sentence.all_sentences.items():
            x_first = worlds.x_first
            y_first = worlds.y_first
            x_last = worlds.x_last
            y_last = worlds.y_last
            width = worlds.width
            height = worlds.height
            text = worlds.text.strip()

            cv2.rectangle(img, (x_first, y_first), (x_last + width, y_last + height), (255,255,255), -1)
            needed_worlds = round((len(translated_worlds) * len(text.split(' '))) / len(all_worlds))

            cv2.putText(img, ' '.join(translated_worlds[:needed_worlds]), (x_first, y_first + 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
            for i in text.split(' '):
                all_worlds.remove(i)    
            translated_worlds = translated_worlds[needed_worlds+1:]
            

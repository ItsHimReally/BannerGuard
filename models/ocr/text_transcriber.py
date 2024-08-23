import easyocr
from autocorrect import Speller

reader = easyocr.Reader(['ru'],
                        model_storage_directory='custom_EasyOCR/model',
                        user_network_directory='custom_EasyOCR/user_network',
                        recog_network='custom') 
char_whitelist = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789,"
spell = Speller('ru')

def text_from_image(path):
    result = reader.readtext(path, detail=0, paragraph=True, allowlist=char_whitelist, text_threshold=0.8)
    return spell(result[0].lower())
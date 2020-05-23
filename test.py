#OCR 기술
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from matplotlib import pyplot as plt
import numpy as np
import random
im = Image.open('screenshot1.png').crop((240, 365, 679, 484))
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(10)
#im = im.convert('1')
im.save('temp2.png')

token = "!.,'-_^*1234567890+="
def addtoken(st):
    out = ""
    for t in st:
        out += t
        if random.choice([True, False]):
            out += token[random.randint(0, len(token)-1)]
    return out
print(addtoken("좆까 씨발새끼야 이미 갤 좆창났어 그냥 꺼져"))

kernel = np.ones((5,5), np.uint8)
im_gray = cv2.imread('temp2.png', cv2.IMREAD_GRAYSCALE)
im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_CLOSE, kernel)
#im_gray = cv2.fastNlMeansDenoising(im_gray, None, 3, 7, 21)
#im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_OPEN, kernel)
(thresh, im_gray) = cv2.threshold(im_gray, 110, 255, cv2.THRESH_BINARY_INV )
im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_OPEN, kernel)
cv2.imwrite("tt.png", im_gray)
_text = pytesseract.image_to_string(im_gray, lang='eng', config='-psm 8 -oem 3 -l eng')

#text = pytesseract.image_to_string(Image.open('temp2.png'))
text = ""
for t in _text:
    if t.isalpha() or t.isdigit():
        text += t

print(":", _text, " :", text)

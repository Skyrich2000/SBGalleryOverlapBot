#OCR 기술
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from matplotlib import pyplot as plt
import numpy as np
import random
im = Image.open('screenshot1.png').crop((374, 660, 805, 770))
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(4)
#im = im.convert('1')
im.save('temp2.png')


kernel1 = np.ones((5, 5), np.uint8)
kernel2 = np.ones((4, 4), np.uint8)

im_gray = cv2.imread('temp2.png', cv2.IMREAD_GRAYSCALE)
height, width = im_gray.shape[:2]
#im_gray = cv2.resize(im_gray, (int(1.3*width), 2*height), interpolation=cv2.INTER_LINEAR)
#im_gray = cv2.fastNlMeansDenoising(im_gray, None, 3, 7, 21)
(thresh, im_gray) = cv2.threshold(im_gray, 110, 255, cv2.THRESH_BINARY_INV )
#im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_CLOSE, kernel1)
im_gray = cv2.morphologyEx(im_gray, cv2.MORPH_OPEN, kernel2)
cv2.imwrite("tt.png", im_gray)
_text = pytesseract.image_to_string(im_gray, lang='eng', config='-psm 8 -oem 3 -l eng')
#text = pytesseract.image_to_string(Image.open('temp2.png'))
text = ""
for t in _text:
    if t.isalpha() or t.isdigit():
        text += t

print(":", _text, " :"+text)

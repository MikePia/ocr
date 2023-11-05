import cv2

import pytesseract
import os

fn = "images/q1.png"
os.path.exists(fn)


def ocr_core(img):
    text = pytesseract.image_to_string(img)
    return text


def get_greyscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def remove_noise(img):
    return cv2.medianBlur(img, 5)


# thresholding
def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


img = cv2.imread(fn)
print("one")
print(ocr_core(img))

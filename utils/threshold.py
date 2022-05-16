import cv2
import numpy as np

from .gray_scale import grayScale as gray

def monoChrome(img, fromCV2 = True, threshold = 127, invert = False):
    if fromCV2:
        try:
            channel = img.shape[2]
        except:
            channel = 1
        if channel == 3:
            grayImg = gray(img,fromCV2)
        elif channel == 1:
            grayImg = img
        mode = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
        newImg = cv2.threshold(grayImg, threshold, 255, mode)[1]
        return newImg

def truncate(img, threshold = 127):
    grayImg = gray(img, fromCV2 = True)
    return cv2.threshold(grayImg, threshold, 255, cv2.THRESH_TRUNC)[1]

def toZero(img, threshold = 127):
    grayImg = gray(img, fromCV2 = True)
    return cv2.threshold(grayImg, threshold, 255, cv2.THRESH_TOZERO)[1]

def toZeroInv(img, threshold = 127):
    grayImg = gray(img, fromCV2 = True)
    return cv2.threshold(grayImg, threshold, 255, cv2.THRESH_TOZERO_INV)[1]

def otsu(img, threshold = 127):
    grayImg = gray(img, fromCV2 = True)
    return cv2.threshold(grayImg, threshold, 255, cv2.THRESH_OTSU)[1]

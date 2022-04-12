import cv2
import numpy as np

from .gray_scale import grayScale as gray

def monoChrome(img, fromCV2 = True, thresh = 127):
    if fromCV2:
        try:
            channel = img.shape[2]
        except:
            channel = 1
        if channel == 3:
            grayImg = gray(img,fromCV2)
        elif channel == 1:
            grayImg = img
        newImg = cv2.threshold(grayImg, thresh, 255, cv2.THRESH_BINARY)[1]
        return newImg

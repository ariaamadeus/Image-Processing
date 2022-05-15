import cv2
import numpy as np

from .gray_scale import grayScale as gray
from .img_converter import rgbgr

def hist(img, gs = True):
    if gs:
        #print(gray(img).shape)
        return [cv2.calcHist(gray(img), 0, None, [256],[0,256])]
    else:
        histlist = []
        for i in range(0,3):
            histlist.append(cv2.calcHist(img, [i], None, [256],[0,256]))
        return histlist

def equalize(img):
    try:
        channel = img.shape[2]
    except:
        channel = 1
    if channel == 1:
        return cv2.equalizeHist(img)
    else:
        return cv2.equalizeHist(gray(img, True))

def clahe(img, clip = 20, grid = (20,20)):
    varClahe = cv2.createCLAHE(clipLimit = clip , tileGridSize = grid)
    try:
        channel = img.shape[2]
    except:
        channel = 1
    if channel == 1:
        return varClahe.apply(img)
    else:
        return varClahe.apply(gray(img,True))

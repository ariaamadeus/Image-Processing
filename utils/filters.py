import cv2
import numpy as np
from .gray_scale import grayScale as gray

def sobel(img):
    try:
        channel = img.shape[2]
    except:
        channel = 1
    if channel == 3:
        img = gray(img,True)
    Sobx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
    Soby = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
    absx = np.absolute(Sobx)
    absy = np.absolute(Soby)
    return np.uint8(absx)+np.uint8(absy)

def horizontal(img):
    kernel1 = np.array(((0,0,0),(-1,2,-1),(0,0,0)))
    return cv2.filter2D(img, -1, kernel1)
 
def bilateral(img, k = 5, sgs = 75, sgr = 75):
    return cv2.bilateralFilter(img, k, sgs, sgr)

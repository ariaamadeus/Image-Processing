import os

import cv2
import numpy as np

def blur(img, kSize=7):
    return cv2.blur(img,(kSize,kSize)).astype(np.uint8)

def gauss(img, kSize=7):
    return cv2.GaussianBlur(img, (kSize,kSize),0).astype(np.uint8)

def median(img, kSize=7):
    return cv2.medianBlur(img, kSize).astype(np.uint8)

__all__ = ['blur,gauss,median']

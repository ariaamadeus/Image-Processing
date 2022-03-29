import os

import cv2
import numpy as np

def blur(img, kSize=5):
    return cv2.blur(img,(kSize,kSize))

def gauss(img, kSize=5):
    return cv2.GaussianBlur(img, (kSize,kSize),0)

def median(img, kSize=5):
    return cv2.medianBlur(img, kSize)

__all__ = ['blur,gauss,median']

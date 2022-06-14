import os

import cv2
import numpy as np

def blur(img, kernel):
    for i, kern in enumerate(kernel):
        if kern % 2 == 0 : 
            kernel[i] += 1
    return cv2.blur(img, kernel).astype(np.uint8)

def gauss(img, kernel):
    for i, kern in enumerate(kernel) :
        if kern % 2 == 0 :
            kernel[i] += 1
    return cv2.GaussianBlur(img, kernel, 0).astype(np.uint8)

def median(img, kernel):
    for i, kern in enumerate(kernel) :
        if kern % 2 == 0 :
            kernel[i] += 1
    return cv2.medianBlur(img, kernel[0]).astype(np.uint8)

__all__ = ['blur,gauss,median']

import os

import cv2
import numpy as np

def blur(img, kernel=(5,5)):
    for i, kern in enumerate(kernel):
        if kern % 2 == 0 : 
            kernel[i] += 1
    return cv2.blur(img, kernel).astype(np.uint8)

def gauss(img, kernel=(5,5)):
    for i, kern in enumerate(kernel) :
        if kern % 2 == 0 :
            kernel[i] += 1
    return cv2.GaussianBlur(img, kernel, 0).astype(np.uint8)

def median(img, kernel=(5,5)):
    try:
        len(kernel)
        for i, kern in enumerate(kernel) :
            if kern % 2 == 0 :
                kernel[i] += 1
        kernel = kernel[0]
    except:
        pass

    return cv2.medianBlur(img, kernel).astype(np.uint8)

__all__ = ['blur,gauss,median']

import os

import cv2
import numpy as np

def grayScale(img, fromCV2 = True):
    if fromCV2:
        newImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return newImg.astype(np.uint8)
    else:
        height, width, channel = img.shape
        newImage = np.zeros(shape=(height,width))

        y = 0
        for piyel in img:
            x = 0
            for pixel in piyel:
                b,g,r = pixel
                newImage[y][x]=int( 0.11*b + 0.59*g + 0.3*r )
                x+=1
            y+=1

        return newImage.astype(np.uint8)

def monoChrome(img, fromCV2 = True, thresh = 127):
    if fromCV2:
        try:
            channel = img.shape[2]
        except:
            channel = 1
        if channel == 3:
            grayImg = grayScale(img,fromCV2)
        elif channel == 1:
            grayImg = img
        newImg = cv2.threshold(grayImg, thresh, 255, cv2.THRESH_BINARY)[1]
        return newImg

import os

import cv2
import numpy as np

def grayScale(img, fromCV2 = True):
    if fromCV2:
        newImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return newImg.astype(np.uint8)
    else:
        height, width, channel = img.shape
        newImage = np.zeros(shape=(height,width,1))

        y = 0
        for piyel in img:
            x = 0
            for pixel in piyel:
                b,g,r = pixel
                newImage[y][x]=int( 0.11*b + 0.59*g + 0.3*r )
                x+=1
            y+=1

        return newImage.astype(np.uint8)


import os

import cv2
import numpy as np
from PIL import Image

#Required for QT x OpenCV
for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        del os.environ[k]

def grayScale(img, fromCV2 = False):
    print("Processing...")
    if fromCV2:
        newImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Done!")
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
                #newImage[y][x][1]=int( 0.11*b + 0.59*g + 0.3*r )
                #newImage[y][x][2]=int( 0.11*b + 0.59*g + 0.3*r )
                #print(newImage[y][x])
                x+=1
            y+=1

        print("Done!")
        return newImage.astype(np.uint8)

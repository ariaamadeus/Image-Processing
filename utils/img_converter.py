import os

import cv2
import numpy as np
from PIL import Image

def openImage(path):
    mode = Image.open(path).mode
    if mode == "L":
        return cv2.imread(path,0), mode
    return cv2.imread(path,1), mode

def rgbgr(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def modeCheck(img):
    return Image.fromarray(img).mode    

def resize(img, scale = 0.7):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img,(width,height))

def saveImage(path, img):
    pathList = path.split('/')
    path = ''
    for x in range(1,len(pathList)-1):
        path += '/' + pathList[x]
    path += '/output.%s' % pathList[len(pathList)-1].split('.')[1]
    cv2.imwrite(path, img)
    return path

if __name__ == "__main__":
    newImage = grayScale(openImage("durian.jpeg"))
    cv2.imshow("frame",newImage)
    cv2.waitKey(0)


import os

import cv2
import numpy as np
from PIL import Image

#Required for QT x OpenCV
for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        del os.environ[k]

def openImage(path): 
    return cv2.imread(path), Image.open(path).mode 

def grayScale(img, fromCV2 = False):
    if fromCV2:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    else:
        height, width, channel = img.shape
        newImage = np.zeros(shape=(height,width,3))

        print("Processing...")

        y = 0
        for piyel in img:
            x = 0
            for pixel in piyel:
                b,g,r = pixel
                newImage[y][x][0]=int( 0.11*b + 0.59*g + 0.3*r )
                newImage[y][x][1]=int( 0.11*b + 0.59*g + 0.3*r )
                newImage[y][x][2]=int( 0.11*b + 0.59*g + 0.3*r )
                #print(newImage[y][x])
                x+=1
            y+=1

        print("Done!")

        return newImage

def one2three(img):
    height, width, channel = img.shape
    newImg = np.zeros(shape=(height,width,3))
    newImg[0] = img
    newImg[1] = img
    newImg[2] = img
    return newImg

def rgbgr(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def resize(img, scale = 0.7):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img,(width,height))

def saveImage(path, img):
    pathList = path.split('/')
    path = ''
    for x in range(1,len(pathList)-1):
        path += '/' + pathList[x]
    path += '/output.jpeg'
    print(path)
    #path = os.path.join(*path)
    cv2.imwrite(path, img)

if __name__ == "__main__":
    newImage = grayScale(openImage("durian.jpeg"))
    cv2.imshow("frame",newImage)
    cv2.waitKey(0)


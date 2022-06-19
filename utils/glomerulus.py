import cv2
import numpy as np

from .blur import median
from .gray_scale import grayScale as gray
from .threshold import inRange, monoChrome 
from .contours import contours, conArea, erode, dilate
from .histogram import clahe

def glomerulus(img):
    imgToMono = img.copy()
    for itter in range(0,5):
        imgToMono = median(imgToMono,(5,5))
    maskGlom0 = inRange(imgToMono, (0,60,185),(7,255,255))
    maskGlom1 = inRange(imgToMono, (0,35,185),(7,255,255))
    imgToMono = clahe(imgToMono)
    imgToMono = erode(imgToMono,(3,3),3)
    imgToMono = dilate(imgToMono,(3,3),2)
    imgToMono = monoChrome(imgToMono)
    imgCont = contours(imgToMono)
    areas = conArea(imgCont)
    #imgTEMP = img.copy()
    #imgTEMP = cv2.drawContours(imgTEMP, imgCont, -1, color = (255,255,0), thickness = 3) 
    #cv2.imwrite("img.jpg",imgTEMP)

    deviasis = {}
    devtotal = 0
    count = 0
    firstMean = cv2.mean(maskGlom1)
    #print("First Mean: ",firstMean)
    for i, area in enumerate(areas):
        if area > 30000 and area < 300000:
            mask = maskGlom1.copy()
            cv2.drawContours(mask, imgCont, i, 0, -1)
            mean = cv2.mean(mask)
            deviasi = firstMean[0] - mean[0]
            deviasis[i] = abs(deviasi)
            devtotal += abs(deviasi)
            count+=1
            #print("Mean%s: "%i, mean,"Deviasi: ", deviasi)
            #cv2.imwrite("Test%s.jpg"%i,mask)
    rata = devtotal/count
    for x in deviasis:
        if deviasis[x] >= rata:
            img = cv2.drawContours(img, imgCont, x, color = (255,255,0), thickness = 3)
    cv2.imwrite("img.jpg",img)
    return img

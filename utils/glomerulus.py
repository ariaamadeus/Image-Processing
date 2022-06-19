import cv2

from .blur import median
from .gray_scale import grayScale as gray
from .threshold import inRange, monoChrome 
from .contours import contours, conArea, erode, dilate
from .histogram import clahe

def glomerulus(img):
    #mask = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
    imgToMono = img.copy()
    for itter in range(0,5):
        imgToMono = median(imgToMono,(5,5))
    maskGlom0 = inRange(imgToMono, (0,60,185),(7,255,255))
    maskGlom1 = inRange(imgToMono, (0,35,185),(7,255,255))
    #maskGlom0 = inRange(mask, (219,165,255),(160,91,177))
    #Efor itter in range(0,5)
    #    imgToMono = median(img,(5,5))
    #imgToMono = gray(imgToMono)
    imgToMono = clahe(imgToMono)
    imgToMono = erode(imgToMono,(3,3),3)
    imgToMono = dilate(imgToMono,(3,3),2)
    #imgMono = monoChrome(imgEroded)
    imgToMono = monoChrome(imgToMono)
    imgCont = contours(imgToMono)
    areas = conArea(imgCont)
    for i, area in enumerate(areas):
        if area > 30000:
            img = cv2.drawContours(img, imgCont, i, color = (255,255,0), thickness = 3)

    #cv2.imwrite("test.jpg",imgToMono)
    return maskGlom1

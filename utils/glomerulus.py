import cv2

from .blur import median
from .gray_scale import grayScale as gray
from .threshold import inRange, monoChrome 
from .contours import erode, dilate
from .histogram import clahe

def glomerulus(img):
    mask = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
    maskGlom0 = inRange(mask, (160,91,17),(219,165,255))
    for itter in range(0,5):
        imgBlur = median(img,(5,5))
    imgGray = gray(imgBlur)
    imgClahe = clahe(imgGray)
    imgEroded = erode(imgClahe)
    imgMono = monoChrome(imgEroded, True, 127, True)
    cv2.imwrite("/home/it2/Desktop/test.jpg",imgMono)



    


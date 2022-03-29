import cv2
from . import gray_scale as gs

def hist(img, gs = True):
    if gs:
        return [cv2.calcHist(img, 0, None, [256],[0,256])]
    else:
        histlist = []
        for i in range(0,3):
            histlist.append(cv2.calcHist(img, [i], None, [256],[0,256]))
        return histlist

def equalize(img):
    if img.shape[2] == 1:
        return cv2.equalizeHist(img)
    else:
        return cv2.equalizeHist(gs.grayScale(img, True))


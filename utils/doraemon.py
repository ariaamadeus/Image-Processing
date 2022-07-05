import os

import cv2
import numpy as np

from .gray_scale import grayScale as gray
from .histogram import clahe
from .blur import median
from .threshold import monoChrome as mono

persons = ["Doraemon","Dorami","Giant","Nobita","Shizuka","Suneo"]
# try:
#     os.chdir("Dorameong/save")
# except:
#     os.mkdir("Dorameong/save")
#     os.chdir("Dorameong/save")

# for person in persons:
#     try:
#         os.chdir(person)
#     except:
#         os.mkdir(person)
#         os.chdir(person)
#     os.chdir("..")

# os.chdir("../..")
global means
means = []

def initial():
    global means
    for i, person in enumerate(persons):
        means.append(_doramean(cv2.imread(f"Dorameong/save/{person}/banding.jpg")))

def _doraemon(img):
    image = img.copy()
    image = image[:,250:400]
    cv2.imwrite("crop.jpg", image)

    toMono = gray(image)
    cv2.imwrite("gray.jpg", toMono)

    for x in range(0,3):
        toMono = median(toMono, (5,5))
    cv2.imwrite("median1.jpg", toMono)
    
    toMono = clahe(toMono)
    cv2.imwrite("clahe.jpg", toMono)
    
    toMono = mono(toMono)
    cv2.imwrite("mono127.jpg", toMono)
    #toMono = otsu(toMono)

    for x in range(0,3):
        toMono = median(toMono, (5,5))
    cv2.imwrite("median2.jpg", toMono)
    return toMono

def _doramean(img):
    image = _doraemon(img)

    imgheight=image.shape[0]
    imgwidth=image.shape[1]

    y1,x1 = (0,0)
    M = imgheight//15
    N = imgwidth//7
    mean = []
    for y in range(0,imgheight,M):
        for x in range(0, imgwidth, N):
            y1 = y + M
            x1 = x + N
            tiles = image[y:y+M,x:x+N]
            mean.append(cv2.mean(tiles))
            cv2.rectangle(image, (x, y), (x1, y1), (0, 255, 0))
            # cv2.imwrite("save/" + str(x) + '_' + str(y)+".png",tiles)
    cv2.imwrite("separate.jpg", image)
    return mean

initial()
def doraemon(img):
    global means
    mean = _doramean(img)
    deviasi = []
    for firstMean in means:
        deviasi.append(abs(sum(np.array(firstMean)-np.array(mean))[0]))
    print(deviasi)
    min_value = min(deviasi)
    min_index=deviasi.index(min_value)
    print(persons[min_index])
    return _doraemon(img)
        
    

import cv2
from cv2 import erode
import numpy as np
from .gray_scale import grayScale as gray
from .threshold import monoChrome as mono
from .contours import contours, conArea, erode, dilate

def kmean(img, K, attempts=5):
    image = img.reshape((-1,3))
    image = np.float32(image)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    attempts = attempts
    compact, labels, centers = cv2.kmeans(image, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
    
    centers[0] = 0 # background putih dibuat hitam
   
    centers = np.uint8(centers)
    count = 1
    for i in range(1,K+1):
        label = labels.flatten()
        label = np.where(label > i,0,label)
        label = np.where(label < i,0,label)
        segmented = centers[label]
        res = segmented.reshape((img.shape))
        mask = mono(gray(res),threshold = 1)
        mask = erode(erode(mask))
        mask = dilate(dilate(mask))
        cnts = contours(mask) 
        areas = conArea(cnts)
        # print(areas)
        cings = []
        count1 = 0
        for j, area in enumerate(areas):
            if area > 2400:
                cings.append(j)
                count1+=1
        
        if count1 == 2:
            for cing in cings:
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                cv2.drawContours(img, cnts, cing, (255,255,255), 2)
            for cnt in cnts:
                # c = max(cnt, key=cv2.contourArea)
                M = cv2.moments(cnt)
                area = conArea([cnt])
                if area[0]>2200:
                    try:
                        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
                        fontScale = 0.5
                        color = (0, 0, 0) #BGR
                        thickness = 2
                        img = cv2.putText(img, '%s'%count, center, font, fontScale, color, thickness, cv2.LINE_AA)
                    except:
                        pass
            count+=1
    
    return img

if __name__  == "__main__":
    image = cv2.imread("Kancing_baju.png")
    cv2.imwrite("test.png",kmean(image,K=11,attempts=5))
    
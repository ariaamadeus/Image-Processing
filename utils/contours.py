import cv2

def connected(img):
    return cv2.connectedComponents(img)

def contours(img, drawImg = [], draw = False, color = (255,255,0), thick = 5):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("Contour Area(s): ",conArea(contours))
    print("Contour Perimeter(s): ",perimeter(contours, closed = True))
    print("Contour Center(s): ", center(contours))
    if draw:
        newImg = drawImg.copy()
        newImg = cv2.drawContours(newImg, contours, -1, color, thickness= thick)
        return newImg
    
    return contours

def conArea(contours):
    areas = []
    for cnt in contours:
        areas.append(cv2.contourArea(cnt))
    return areas

def perimeter(contours, closed = True):
    perimeters = []
    for cnt in contours:
        perimeters.append(cv2.arcLength(cnt, closed))
    return perimeters

def center(contours):
    centers = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if not M['m00'] : continue
        centers.append(
            [M["m10"]/M["m00"],
            M["m01"]/M["m00"]
            ])
    return centers

def erode(img, kernel = (5,5), itterations = 1):
    return cv2.erode(img, kernel, itterations)

def dilate(img, kernel = (5,5), itterations = 1):
    return cv2.dilate(img, kernel, itterations)

def opening(img, kernel = (5,5), itterations = 1):
    for x in range(0,itterations):
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img

def closing(img, kernel = (5,5), itterations = 1):
    for x in range(0,itterations):
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

def gradient(img, kernel = (5,5), itterations = 1):
    for x in range(0,itterations):
        img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    return img
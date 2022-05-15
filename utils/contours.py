import cv2

def connected(img):
    return cv2.connectedComponents(img)

def contours(img, draw = False, color = (255,255,0), thick = 5):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if draw:
        #for cnt in contours:
        img = cv2.drawContours(img, contours, 0, color, thickness= thick)
        return img
    return contours

def conArea(contour):
    return cv2.contourArea(contour)

def perimeter(contour, closed = True):
    return cv2.arcLength(contour, closed)

def center(contour):
    M = cv2.moments(contour)
    x = M["m10"]/M["m00"]
    y = M["m01"]/M["m00"]
    return x,y

def erode(img, kernel, itterations):
    return cv2.erode(img, kernel, itterations)

def dilate(img, kernel, itterations):
    return cv2.dilate(img, kernel, itterations)

def opening(img, kernel, itterations):
    for x in range(0,itterations):
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img

def closing(img, kernel, itterations):
    for x in range(0,itterations):
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

def gradient(img, kernel, itterations):
    for x in range(0,itterations):
        img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    return img
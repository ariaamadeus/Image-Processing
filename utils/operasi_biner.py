import cv2

def labeling(image):
    return cv2.connectedComponents(image)

def contours(image):
    return
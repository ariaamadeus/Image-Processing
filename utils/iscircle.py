import cv2
import numpy as np

def iscircle(img):
    image = inRange(img,(0,0,210),(1,0,212))
    # cv2.imwrite("test.jpg",image)
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1, 30, param1=200, param2=10, minRadius=1, maxRadius=30)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        font = cv2.FONT_HERSHEY_SIMPLEX
        org1 = (i[0]+10, i[1]-15)
        org2 = (i[0]+10, i[1])
        org3 = (i[0]+10, i[1]+15)
        fontScale = 0.5
        color = (0, 0, 255) #BGR
        thickness = 1
        img = cv2.putText(img, f'(x:{i[0]},', org1, font, fontScale, color, thickness, cv2.LINE_AA)
        img = cv2.putText(img, f'y:{i[1]},', org2, font, fontScale, color, thickness, cv2.LINE_AA)
        img = cv2.putText(img, f'r:{i[2]})', org3, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),1,(0,0,255),3)
    return img

if __name__ == "__main__":
    from threshold import inRange
    image = cv2.imread("PCB2.png")
    cv2.imwrite("output.png",iscircle(image))
else:
    from .threshold import inRange
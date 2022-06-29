import cv2 as cv
import numpy as np

def nothing(x):
    pass

capture = cv.VideoCapture(1)
window_name = ["Camera", "Binary"]
img, hsv_img, hsv_split, binary = 0, 0, 0, 0

i = 0
while(i < len(window_name)):
    cv.namedWindow(window_name[i], cv.WINDOW_AUTOSIZE)
    i += 1

lowerb, upperb = 100, 109
cv.createTrackbar("lb", window_name[1], lowerb, 255, nothing)
cv.createTrackbar("ub", window_name[1], upperb, 255, nothing)
#
while(cv.waitKey(20) != 27):
    ret, frame = capture.read()
    if ret == False:
        break
    img = frame.copy()

    lowerb = int(cv.getTrackbarPos("lb", window_name[1]))
    upperb = int(cv.getTrackbarPos("ub", window_name[1]))

    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv_split = cv.split(hsv_img)
    binary = cv.inRange(hsv_split[0], lowerb, upperb)
    binary = cv.blur(binary, (3, 3))
    elemet = np.ones((3, 3), np.uint8)
    binary = cv.erode(binary, elemet)

    cont = binary.copy()
    contours, hierarchy = cv.findContours(cont, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max = 0
    i_cont = -1
    i = 0
    while(i < len(contours)):
        if(cv.contourArea(contours[i]) > max):
            max = np.abs(cv.contourArea(contours[i]))
            i_cont = i
        i += 1
    if(i_cont >= 0):
        contours_poly = cv.approxPolyDP(contours[i_cont], 3, True)
        x,y,w,h = cv.boundingRect(contours_poly)
        cv.rectangle(img, (x,y), (x+w, y+h),(125, 250, 125), 2)
        cv.drawContours(img, contours, i_cont, (0, 0, 255), 2)

    cv.imshow(window_name[0], img)
    cv.imshow(window_name[1], binary)

capture.release()
cv.destroyAllWindows()
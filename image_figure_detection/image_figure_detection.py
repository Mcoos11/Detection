import cv2
import numpy as np

obraz = cv2.imread("images/image.jpg")

#przygotowanie obrazu
# obraz2 = cv2.cvtColor(obraz, cv2.COLOR_RGB2GRAY) #zmienia na szary
# obraz2 = cv2.GaussianBlur(obraz2, (5, 5), 0) #rozmycie gaussowskie o masce 5x5
# _, prog = cv2.threshold(obraz2, 0, 16, cv2.THRESH_BINARY) #progowanie (min, max, tryb)

hsv_img = cv2.cvtColor(obraz, cv2.COLOR_RGB2HSV)
hsv_split = cv2.split(hsv_img)
binary = cv2.inRange(hsv_split[0], 25, 180)
binary = cv2.blur(binary, (3, 3))
elemet = np.ones((3, 3), np.uint8)
prog = cv2.erode(binary, elemet)
#
#podisywanie
czcionka = cv2.FONT_HERSHEY_SIMPLEX

#konturowanie
knt,_ = cv2.findContours(prog, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #konturowanie (obraz, tryb, tryb)
for k in knt:
    x, y, w, h = cv2.boundingRect(k) #parametry konturu
    if w > 10 and h > 10:
        if x == 0 and y == 0:
            continue
        rogi = cv2.approxPolyDP(k, 0.02 * cv2.arcLength(k, True), True) #detekcja ksztaltow zamknietych (parametry, dokladnosc)

        #sprawdzanie ksztaltow
        if len(rogi) == 4:
            kol = [255, 0, 0]
            tekst = "kwadrat"
            cv2.drawContours(obraz, [rogi], 0, kol, 2)  # rysowanie obramowania
            cv2.putText(obraz, tekst, [x, y], czcionka, 0.7, [100, 100, 100], 2)
        elif len(rogi) == 3:
            kol = [0, 255, 0]
            tekst = "trojkąt"
            cv2.drawContours(obraz, [rogi], 0, kol, 2)  # rysowanie obramowania
            cv2.putText(obraz, tekst, [x, y], czcionka, 0.7, [100, 100, 100], 2)
        elif len(rogi) == 8:
            kol = [0, 255, 255]
            tekst = "okrag"
            cv2.drawContours(obraz, [rogi], 0, kol, 2)  # rysowanie obramowania
            cv2.putText(obraz, tekst, [x, y], czcionka, 0.7, [100, 100, 100], 2)

cv2.imshow("wyjscie", obraz)
cv2.imshow("progowanie", prog)
cv2.waitKey(0)

cv2.destroyAllWindows()
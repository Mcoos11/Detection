import numpy as np
import cv2

def label(image, c):
	# maska konturu, srednia wartosc kolorow
	image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = np.zeros(image.shape[:2], dtype="uint8")
	cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)
	mask = cv2.erode(mask, None, iterations=2)
	mean = cv2.mean(image_hsv, mask=mask)[0]
	# print("sredni kolor: " + str(mean))

	# sprawdzanie koloru
	if((mean >= 0 and mean <= 12) or (mean >= 345 and mean <= 360)):
		color = ["red", mean]
	elif(mean >= 14 and mean <= 70):
		color = ["yellow", mean]
	elif(mean >= 80 and mean <= 273):
		color = ["blue", mean]
	else:
		color = ["other", mean]

	# zwrot nazwy koloru
	return color



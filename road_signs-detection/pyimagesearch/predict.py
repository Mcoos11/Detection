from pyimagesearch.shapedetector import ShapeDetector
import pyimagesearch.colorlabeler as col
import matplotlib.pyplot as plt
import imutils
import cv2
import numpy as np
import os

def prediction(tree, file_name):
	in_path = os.path.join("./test", file_name)
	image = cv2.imread(in_path)
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	# blur i resize, konwert na kolory L*A*B i RGB
	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	# thresh = cv2.inRange(gray, 150, 200)
	thresh = cv2.inRange(gray, 25, 180)
	# cv2.imshow("name", thresh)

	# znajdowanie konturow
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	sd = ShapeDetector()

	# sprawdzanie konturow
	for c in cnts:
		x, y, w, h = cv2.boundingRect(c)  # parametry konturu
		if w > 60 and h > 60:
			if x == 0 and y == 0:
				continue
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			# srodek konturu
			M = cv2.moments(c)
			cX = int((M["m10"] / (M["m00"] + 0.0001)) * ratio)
			cY = int((M["m01"] / (M["m00"] + 0.0001)) * ratio)

			# znalezienie nazwy ksztaltu i koloru
			color = col.label(image, c)
			shape = sd.detect(c)

			# rozpoznawanie
			data = np.array([[int(color[1]), shape[1]]])
			out = tree.predict(data)
			if(out == [[1]]):
				out_str = "ostrzegawczy"
			elif(out == [[2]]):
				out_str = "nakazu"
			elif(out == [[3]]):
				out_str = "zakazu"
			elif(out == [[4]]):
				out_str = "informacyjny"
			print("wynik: " + out_str)

			# zaznaczenie ksztaltu, obrysowanie go i opisanie
			text = "{}".format(out_str)
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, text, (int(cX/ratio), int(cY/ratio)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 168, 22), 2)

			# zwrot zdjecia z zaznaczonymi rzeczami
			cv2.imshow("Image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			#zaznaczanie na wykresie
			plt.figure(2)
			plt.plot(data[0][0], data[0][1], 'ko', zorder=2)
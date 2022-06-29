from pyimagesearch.shapedetector import ShapeDetector
import pyimagesearch.colorlabeler as col
import imutils
import cv2
import csv

#plik wyjsciowy
def csv_writer(data, path):
	with open('data.csv', 'a', encoding='utf8', newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter = ';')
		writer.writerow(data)
		csv_file.close()

def gen_data():
	print("ile znkakow w folderze: ")
	n = input()

	#nazwy kolumn w pliku wyjsciowym
	with open('data.csv', 'w', encoding='utf8', newline='') as csv_file:
		writer = csv.DictWriter(csv_file, delimiter = ';', fieldnames=["color", "shape", "type"])
		writer.writeheader()
		csv_file.close()

	j = 0
	while(j < 4):
		if j == 0:
			type = "ostrzegawcze"
		elif j == 1:
			type = "nakazu"
		elif j == 2:
			type = "zakazu"
		elif j == 3:
			type = "informacyjne"
		i = 0
		while(i < int(n)):
			in_path = "znaki/" + type + "/" + str(i+1) + ".png"
			i += 1
			image = cv2.imread(in_path)
			resized = imutils.resize(image, width=300)
			ratio = image.shape[0] / float(resized.shape[0])

			# blur i resize, konwert na kolory L*A*B i RGB
			blurred = cv2.GaussianBlur(resized, (5, 5), 0)
			gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
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
					# M = cv2.moments(c)
					# cX = int((M["m10"] / (M["m00"] + 0.0001)) * ratio)
					# cY = int((M["m01"] / (M["m00"] + 0.0001)) * ratio)

					# znalezienie nazwy ksztaltu i koloru
					color = col.label(image, c)
					shape = sd.detect(c)

					#zapis do pliku
					out = [int(color[1]), shape[1], j+1]
					csv_writer(out, "data.csv")
		j += 1
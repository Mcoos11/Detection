import cv2

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		# inicjacja nazwy ksztaltu i przyblizenie konturu
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		# sprawdzanie ile ma krawedzi
		if len(approx) == 3:
			shape = ["triangle", 11]

		elif len(approx) == 4:
			shape = ["rectangle", 12]

		# gdy ma wiecej krawedzi to chyba kolo
		else:
			shape = ["circle", 13]

		# zwrot nazwy ksztaltu
		return shape
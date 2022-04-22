from typing import List
import numpy as np
import cv2.cv2 as cv2
from Vehicle import Vehicle


class Detector:
    def __init__(self):
        pass

    @staticmethod
    def detect_vehicles(img: np.ndarray, row: int, col: int) -> List[Vehicle]:

        """Detect vehicles in sub-image with color filter.
        param np.ndarray img: The image where detection will be.
        param int row: Padding row.
        param int col: Padding col.
        :return: List with all detected vehicles."""

        # segmented_image = detect_road(img)

        ilowH = 40
        ihighH = 100

        ilowS = 20
        ihighS = 55
        ilowV = 10
        ihighV = 90

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_hsv = np.array([ilowH, ilowS, ilowV])
        higher_hsv = np.array([ihighH, ihighS, ihighV])
        output_mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        output_mask = cv2.erode(output_mask, kernel=kernel, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        output_mask = cv2.dilate(output_mask, kernel=kernel, iterations=1)

        linesP = cv2.HoughLinesP(output_mask, 1, np.pi / 180, 50, None, 50, 10)

        if linesP is not None:
            for i in range(0, len(linesP)):
                line = linesP[i][0]
                cv2.line(output_mask, (line[0], line[1]), (line[2], line[3]), (0, 0, 0), 3, cv2.LINE_AA)

        # Detectar los distintos contornos que aparecen en la imagen y quedarse
        # con aquel que presente mayor área
        contours, _ = cv2.findContours(output_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        area_max = 40
        area_min = 15
        vehicles = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (area_min <= w <= area_max) and (area_min <= h <= area_max) and np.abs(h - w) < 7:
                vehicles.append(Vehicle(y + row, x + col, w, h))

        return vehicles

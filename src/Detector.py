from typing import List
import numpy as np
import cv2.cv2 as cv2
from Vehicle import Vehicle


# Extraer segmentos grandes para las carreteras
def extractLargerSegment(maskROAD):
    contours, _ = cv2.findContours(maskROAD.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    maxA = 0
    maskTemp = np.zeros_like(maskROAD)

    if len(contours) > 0:
        for h, cnt in enumerate(contours):
            if cv2.contourArea(cnt) > maxA:
                cntMax = cnt
                maxA = cv2.contourArea(cnt)
        mask = np.zeros(maskROAD.shape, np.uint8)
        cv2.drawContours(maskTemp, [cntMax], 0, 255, -1)
        maskROAD = cv2.bitwise_and(maskROAD, maskTemp)
    return maskROAD


# Procesamos la imagen para quitar los trozos que no son de carreteras
def post_process(img):
    kernel = np.ones((5, 5), np.uint8)
    img_out = cv2.erode(img, kernel, iterations=3)
    kernel = np.ones((20, 20), np.uint8)
    img_out = cv2.dilate(img_out, kernel, iterations=5)

    img_out = extractLargerSegment(img_out)

    return img_out


# Detectar con un filtro de color qué zonas de la imagen es una carretera
def detect_road(img: np.ndarray) -> np.ndarray:
    ilowH = 40
    ihighH = 100

    ilowS = 20
    ihighS = 60
    ilowV = 10
    ihighV = 90

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([ilowH, ilowS, ilowV])
    higher_hsv = np.array([ihighH, ihighS, ihighV])
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
    mask = post_process(mask)
    img_segmented = img.copy()
    img_segmented[mask == 0] = (0, 0, 0)
    return img


def detect_vehicles(img: np.ndarray, row: int, col: int) -> List:
    """
    Detect vehicles in sub-image with color filter.
    param np.ndarray img: The image where detection will be.
    param int row: Padding row.
    param int col: Padding col.
    :return: List with all detected vehicles.
    """

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
            l = linesP[i][0]
            cv2.line(output_mask, (l[0], l[1]), (l[2], l[3]), (0, 0, 0), 3, cv2.LINE_AA)

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

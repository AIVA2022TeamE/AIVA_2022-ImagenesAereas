from typing import List
import numpy as np
import YoloDetector
# import map_slicer


class TrafficDetector:
    def __init__(self, img: np.ndarray):
        """
        TrafficDetector constructor.
        """
        self._img = img
        # self._coordinates = None
        self._vehicles = []
        self._detector = YoloDetector.YoloDetector()    

    def get_cars_from_image(self) -> List:
        """
        Recognize vehicles in image.
        :return: the list with all detected vehicles.
        """
        self._slide()

        # Flatten list
        self._vehicles = [val for sublist in self._vehicles for val in sublist]
        return self._vehicles

    def _slide(self):
        """
        Iterates around the image and calls Detector to detect vehicles in sub-image.
        """

        STEP = 500
        rows, cols = self._img.shape[:-1]
        slides = int((cols / STEP) * (rows / STEP))
        i = 1
        for col in range(0, cols, STEP):
            for row in range(0, rows, STEP):
                print(f"Slide {i}/{slides}", flush=True)
                i += 1
                vehicles = self._detector.detect_vehicles(
                    self._img[row: row + STEP, col: col + STEP], row, col
                )
                self._vehicles.append(vehicles)
    
    def get_cars_density_from_image(self):
        return len(self._vehicles) / (self._img.shape[0] * self._img.shape[1])

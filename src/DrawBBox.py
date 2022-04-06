from typing import List
import Vehicle
import cv2 as cv
import numpy as np


class DrawBBox:
    @staticmethod
    def draw(image: np.ndarray, vehicles: List) -> np.ndarray:
        """
        Draw all vehicles in image.
        :param np.ndarray image: The image witch will be used.
        :param List vehicles: The list of all the vehicles.
        """
        for v in vehicles:
            row, col, width, height = v.get_image_info()

            # Draw rectangle
            cv.rectangle(image, (col, row), (col + width, row + height), (0, 0, 255), thickness=2)

        return image

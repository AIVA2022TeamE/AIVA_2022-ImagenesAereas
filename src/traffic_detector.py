from typing import List, Tuple
import numpy as np


class TrafficDetector:
    def __init__(self, nn):
        """
        TrafficDetector constructor.
        :param NeuralNetwork nn: the neural network which we will use.
        """
        self._img = None
        self._coordinates = None
        self._nn = nn  # Neural Network
        self._vehicles = []

    def get_cars_number_from_image(self, img: np.ndarray, coordinates: Tuple) -> List:
        """
        Recognize vehicles in image.
        :param np.ndarray img: The target image.
        :param tuple coordinates: The coordinates of the image.
        :return: the list with all detected vehicles.
        """
        self._img = img
        self._slide()

        # Flatten list
        self._vehicles = [val for sublist in self._vehicles for val in sublist]
        return self._vehicles

    def _slide(self):
        """
        Iterates around the image and calls NN to detect vehicles in sub-image.
        """

        STEP = 250

        cols, rows = self._img.shape[:-1]

        for col in range(0, cols, STEP):
            for row in range(0, rows, STEP):
                vehicles = self._nn.detect_vehicles(
                    self._img[row: row + STEP, col: col + STEP], row, col
                )
                self._vehicles.append(vehicles)

    @staticmethod
    def get_cars_density_from_image(self):
        return len(self._vehicles)/(self._img.shape[0] * self._img.shape[1])

from typing import Tuple


class Vehicle:
    def __init__(self, row: int, col: int, width: int, height: int):
        self._row = row
        self._col = col
        self._width = width
        self._height = height
        self._coordx = None
        self._coordy = None

    def set_coordinates(self, x: float, y: float):
        """
        Set coordinates in Vehicle object.
        :param float x: x coordinate (West-East).
        :param float y: y coordinate (North-South).
        """
        self._coordx = x
        self._coordy = y

    def get_image_info(self) -> Tuple:
        """
        Returns Vehicle image info.
        :return: row, col, width, height
        """
        return self._row, self._col, self._width, self._height

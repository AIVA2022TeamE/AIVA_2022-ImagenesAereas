from typing import List

import numpy as np

from .keras_retinanet import models
from .keras_retinanet.utils.gpu import setup_gpu
from .keras_retinanet.utils.image import preprocess_image, resize_image

from .Vehicle import Vehicle


class Detector:
    def __init__(self, path_to_model: str = "./model/model.h5", score: float = 0.5):
        """
        Detector will use RetinaNet to detect vehicles.
        :param str path_to_model: The path where the model is stored.
        :param float score: Score of confidance. 0.5 by default.
        """

        # select GPU
        gpu = "0"
        setup_gpu(gpu)

        # Load RetinaNet model
        self._model = models.load_model(path_to_model, backbone_name="resnet50")

        # Set score confidance
        self._score = score

    def detect_vehicles(self, img: np.ndarray, row: int, col: int) -> List:
        """
        Detect vehicles in sub-image.
        :param np.ndarray img: The image where detection will be. Must be (250x250x3).
        :param int row: Padding row.
        :param int col: Padding col.
        :return: List with all detected vehicles.
        """

        # Preprocess image
        image = preprocess_image(img)
        image, scale = resize_image(image)

        # Predict Vehicles
        boxes, scores, labels = self._model.predict_on_batch(
            np.expand_dims(image, axis=0)
        )

        # Scale boxes
        boxes /= scale

        # Generate Tree objects
        vehicles = []
        for box, score, _ in zip(boxes[0], scores[0], labels[0]):
            # Boxes are sorted from 1->0
            if score < 0.5:
                break

            box = box.astype(int)

            x1, y1, x2, y2 = box
            # print(x1, y1, x2, y2)
            width = x2 - x1
            height = y2 - y1
            vehicles.append(Vehicle(y1 + row, x1 + col, width, height))

        return vehicles
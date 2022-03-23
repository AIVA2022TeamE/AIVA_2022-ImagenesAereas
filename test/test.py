from src.traffic_detector import TrafficDetector
from src.map_slicer import MapSlicer
import unittest
import cv2.cv2 as cv2
import numpy as np
import os

current_path = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_path, '../data/test/')


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TD = TrafficDetector()
        cls.MS = MapSlicer()

    def test_coordinates_to_pixel(self):
        """
        Test pixel from given coordinates. Pixel must be in accepted region [(382, 187), (437, 274)]
        """
        coordinates = (30.230360, -97.788103)
        image = "austin1.tif"

        w, h = self.MS.get_pixel_from_coordinates(image, coordinates)

        # First point
        str_error = f'Pixel ({w, h})out of bounds (382, 187), (437, 274) for given coordenates: ' \
                    f'(30.230360, -97.788103)'
        self.assertGreater(w, 382, str_error)
        self.assertGreater(h, 187, str_error)

        # Second point
        self.assertLess(w, 437, str_error)
        self.assertLess(h, 274, str_error)

    def test_street_coordenates(self):
        """
        Test MapSlicer returns any coordinates given street name.
        """
        street_name = "West 27th street, Austin"
        coordenates = self.MS.get_street_location(street_name)

        self.assertGreater(len(coordenates), 0)

    def test_number_cars(self):
        """
        Test for checking the number of cars detected by TrafficDetector.
        """
        image = cv2.imread(test_data_dir + 'slice-test-number-cars.png')
        n_cars = self.TD.get_cars_number_from_image(image)
        # Pass: +-1 cars
        self.assertGreater(n_cars, 6)
        self.assertLess(n_cars, 8)

    def test_street_surface(self):
        """
        Test for checking
        """
        image_complete = test_data_dir + 'street-surface-unmask.png'
        image_mask = test_data_dir + 'street-surface-masked.png'

        img_compl = cv2.imread(image_complete)
        img_mask = cv2.imread(image_mask)

        surface_gt = len(np.nonzero(img_mask[:, :, 0])[0])  # surface = 58705
        surface = self.MS.get_street_surface(img_compl)

        # Pass: surface +-5000 pixels
        self.assertGreater(surface, surface_gt - 5000, 'Surface detected for street is too small')
        self.assertLess(surface,  surface_gt + 5000, 'Surface detected for street is too big')


if __name__ == '__main__':
    # Test sets
    test_results = unittest.TestSuite()
    test_results.addTest(Test('test_coordinates_to_pixel'))
    test_results.addTest(Test('test_street_coordenates'))
    test_results.addTest(Test('test_number_cars'))
    test_results.addTest(Test('test_street_surface'))

    # Test launch
    unittest.TextTestRunner().run(test_results)
    unittest.main()

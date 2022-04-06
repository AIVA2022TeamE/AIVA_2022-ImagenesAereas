import os
import sys
import unittest
import cv2.cv2 as cv2
import numpy as np

current_path = os.path.dirname(os.path.abspath(__file__))
list_paths = [os.sep.join([current_path, os.pardir, 'src']), os.sep.join([current_path, os.pardir])]
for path in list_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

from TrafficDetector import TrafficDetector
from MapSlicer import MapSlicer


test_data_dir = os.path.join(current_path, '../data/')


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.MS = MapSlicer()

    def test_coordinates_to_pixel(self):
        """
        Test pixel from given coordinates. Pixel must be in accepted region [(382, 187), (437, 274)]
        """
        coordinates = (30.218193, -97.7859167)
        image = os.sep.join([test_data_dir, "austin1.tif"])
        gt_pixel = (1133, 4722)

        h, w = self.MS.get_pixel_from_coordinates(image, coordinates)

        str_error = f'Pixel ({w, h})out of bounds {gt_pixel} for given coordenates: ' \
                    f'{coordinates}'
        self.assertEqual(h, gt_pixel[0], str_error)
        self.assertEqual(w, gt_pixel[1], str_error)


    def test_street_coordenates(self):
        """
        Test MapSlicer returns any coordinates given street name.
        """
        street_name = "Lark Cove, austin"
        coordenates = self.MS.get_street_box_in_coordinates(street_name)

        self.assertGreater(len(coordenates), 0)

    def test_number_cars(self):
        """
        Test for checking the number of cars detected by TrafficDetector.
        """
        image = cv2.imread(test_data_dir + 'image21.png')
        TD = TrafficDetector(image)
        cars_list = TD.get_cars_from_image()
        # Pass: +-1 cars
        self.assertGreater(len(cars_list), 6)
        self.assertLess(len(cars_list), 12)

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

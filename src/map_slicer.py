class MapSlicer:
    def __init__(self):
        pass

    def get_street_location(self, street):
        return [[-97.7411979, 30.2919317],
                [-97.741777,30.2919729],
                [-97.7417983,30.2919744],
                [-97.741911,30.2919824],
                [-97.7419781,30.2919872],
                [-97.7427637,30.2920431]]

    def get_street_box_in_coordinates(self, street):
        return [30.291824, 30.2919041, -97.740035, -97.738927]

    def get_pixel_from_coordinates(self, image, coordinates):
        # For coordinates 30.220904, -97.786998
        return 411, 237

    def get_street_box_in_pixels(self, image, street):
        return [(382, 187), (437, 274)]

    def get_street_surface(self, image):
        return 58705



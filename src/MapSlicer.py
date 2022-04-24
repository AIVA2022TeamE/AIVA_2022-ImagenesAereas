from osgeo import osr, gdal
import requests
import cv2.cv2 as cv2


class MapSlicer:
    def __init__(self):
        pass

    def get_street_box_in_coordinates(self, street):
        """
        Returns the coordinates of the street in the image
        """
        # Request coordenates to api
        response = requests.get('https://nominatim.openstreetmap.org/search?q='
                                + street.replace(' ', '+') + '&format=json')

        # Get bounding box
        [minlat, maxlat, minlon, maxlon] = response.json()[0]["boundingbox"]
        [minlat, maxlat, minlon, maxlon] = [
            float(minlat), float(maxlat), float(minlon), float(maxlon)]
        return [(minlat, minlon), (maxlat, maxlon)]

    def get_pixel_from_coordinates(self, image, coordinates):
        [(minx, miny), (maxx, maxy)] = self.get_coordenates_from_image(image)

        h, w = 5000, 5000  # size of the image
        x = h - int((coordinates[0] - minx) / (maxx - minx) * h)
        y = int((coordinates[1] - miny) / (maxy - miny) * w)

        return y, x  # lat is y, lon is x

    def get_coordenates_from_image(self, image):
        ds = gdal.Open(image)
        assert ds is not None

        old_cs = osr.SpatialReference()
        old_cs.ImportFromWkt(ds.GetProjectionRef())

        # create the new coordinate system
        wgs84_wkt = """
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG","7030"]],
                AUTHORITY["EPSG","6326"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4326"]]"""
        new_cs = osr.SpatialReference()
        new_cs.ImportFromWkt(wgs84_wkt)

        # create a transform object to convert between coordinate systems
        transform = osr.CoordinateTransformation(old_cs, new_cs)

        # get the point to transform, pixel (0,0) in this case
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        minx = gt[0]
        miny = gt[3] + width*gt[4] + height*gt[5]
        maxx = gt[0] + width*gt[1] + height*gt[2]
        maxy = gt[3]

        # get the coordinates in lat long
        latlong_min = transform.TransformPoint(minx, miny)
        latlong_max = transform.TransformPoint(maxx, maxy)

        return [latlong_min[:-1], latlong_max[:-1]]

    def get_street_image(self, image, street, output_path=None):
        # Read image with opencv
        img = cv2.imread(image)
        coordenates_bbox = self.get_street_box_in_coordinates(street)

        # Get pixel coordenates
        min_x, min_y = self.get_pixel_from_coordinates(
            image, coordenates_bbox[0])
        max_x, max_y = self.get_pixel_from_coordinates(
            image, coordenates_bbox[1])

        # Crop image
        cropped_img = img[max_y-50:min_y, min_x-30:max_x+40, :]

        # Save image
        if output_path is not None:
            cv2.imwrite(f"{output_path}/cropped.jpg", cropped_img)

        return cropped_img

    def get_street_surface(self, image):
        # TODO: Get surface of street
        return 58705


if __name__ == "__main__":
    m = MapSlicer()
    # print(m.get_image_in_coordenates("data/austin1.tif"))
    coordenates_bbox_clawson = m.get_street_box_in_coordinates(
        "Lark Cove, austin")
    print(coordenates_bbox_clawson)
    print(m.get_pixel_from_coordinates(
        "images/austin1.tif", coordenates_bbox_clawson[0]))
    print(m.get_pixel_from_coordinates(
        "images/austin1.tif", coordenates_bbox_clawson[1]))

    m.get_street_image("images/austin1.tif", "Green Forest Dr, austin", "images")

import os
import cv2.cv2 as cv
import TrafficDetector
import DrawBBox
import argparse
from MapSlicer import MapSlicer


class Principal:
    def __init__(self, input_dir, output_dir, street_name):
        self.input = input_dir
        self.output = output_dir
        self.street_name = street_name
        os.makedirs(self.output, exist_ok=True)

    def main(self):
        if self.street_name is None:
            assert os.path.isdir(self.input), f"Input directory does not exist (default: /app/data). Directory given: {self.input}"
            filenames = [f for f in os.listdir(self.input) if os.path.isfile(os.path.join(self.input, f))]
        else:
            assert os.path.isfile(os.path.abspath(self.input)), f"Input image does not exist. Image given: {os.path.abspath(self.input)}"
            self.input = os.path.abspath(self.input)
            filenames = [self.input]

        if not os.path.isdir(self.output):
            os.makedirs(self.output)

        for filename in filenames:
            # Get image
            if self.street_name is not None:
                map_slicer = MapSlicer()
                image = map_slicer.get_street_image(filename, self.street_name, output_path=self.output)
            else:
                image = cv.imread(os.path.join(self.input, filename))

            # Detect Traffic
            vehicle_detector = TrafficDetector.TrafficDetector(image)
            vehicles = vehicle_detector.get_cars_from_image()
            draw_bbox = DrawBBox.DrawBBox()
            output_image = draw_bbox.draw(image, vehicles)

            print(self.output + "/" + filename)
            output_filename = filename.split("/")[-1].split(".")[0] + "_detected.jpg"
            output_name = os.path.join(self.output, output_filename)
            cv.imwrite(output_name, output_image)
            cv.destroyAllWindows()


if __name__ == "__main__":
    # python Principal.py --input /app/data --output /app/data/output --street_name "Green Forest Dr, austin"

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="/app/data", help="Directory to where the images are located. If street_name is given, \
        input must be the file where the street is located")
    ap.add_argument("--street_name", help="Name of the street to be processed. (Include city name also). If is given, input must be a file.")
    ap.add_argument("--output", default="/app/data/output", help="path to where the output images will be located")
    args = vars(ap.parse_args())
    input_path = args['input']
    output_path = args['output']
    street = args['street_name']
    principal = Principal(input_path, output_path, street)
    principal.main()

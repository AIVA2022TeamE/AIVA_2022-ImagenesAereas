import os
import cv2.cv2 as cv
import TrafficDetector
import DrawBBox
import argparse


class Principal:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        os.makedirs(self.output, exist_ok=True)

    def main(self):
        for filename in os.listdir(self.input):
            image = cv.imread(os.path.join(self.input, filename))
            vehicle_detector = TrafficDetector.TrafficDetector(image)
            vehicles = vehicle_detector.get_cars_from_image()
            draw_bbox = DrawBBox.DrawBBox()
            output_image = draw_bbox.draw(image, vehicles)
            cv.imshow(filename, output_image)
            cv.waitKey(0)
            cv.imwrite(self.output + "/" + filename, output_image)
            cv.destroyAllWindows()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="path to where the images are located")
    ap.add_argument("--output", required=True, help="path to where the output images will be located")
    args = vars(ap.parse_args())
    input_path = args['input']
    output_path = args['output']
    principal = Principal(input_path, output_path)
    principal.main()

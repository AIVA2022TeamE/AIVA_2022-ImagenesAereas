import os
import cv2.cv2 as cv
import traffic_detector
import DrawBBox

folder = "../images/austin"

for filename in os.listdir(folder):
    image = cv.imread(os.path.join(folder, filename))
    vehicle_detector = traffic_detector.TrafficDetector()
    vehicles = vehicle_detector.get_cars_number_from_image(image)
    draw_bbox = DrawBBox.DrawBBox()
    output = draw_bbox.draw(image, vehicles)
    cv.imshow(filename, output)
    cv.waitKey(0)
    cv.imwrite("../images/output/" + filename, output)
    cv.destroyAllWindows()

import torch
from Vehicle import Vehicle


class YoloDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect_vehicles(img, row, col):
        """Detect vehicles in sub-image with yolo detector.
        param np.ndarray img: The image where detection will be.
        param int row: Padding row.
        param int col: Padding col.
        :return: List with all detected vehicles."""

        model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolo_opencv/best.pt')  # local model
        # Inference
        print(f"Img shape: {img.shape}")
        results = model(img, size=500)
        value = results.xyxy[0]
        vehicles = []
        for tensor in value:
            # Move numpy if tensor if in gpu
            vehicle = tensor.numpy() if 'cpu' in str(tensor.device) else tensor.cpu().numpy()
            r_min = int(vehicle[1]) + row
            c_min = int(vehicle[0]) + col
            r_max = int(vehicle[3]) + row
            c_max = int(vehicle[2]) + col
            vehicles.append(Vehicle(r_min, c_min, r_max, c_max))

        return vehicles

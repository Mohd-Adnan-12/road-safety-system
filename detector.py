from ultralytics import YOLO
import cv2

class VehicleDetector:
    def __init__(self, model_path="models/yolov8n.pt", conf=0.5):
        self.model = YOLO(model_path)
        self.conf = conf
        self.vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

    def detect(self, frame):
        results = self.model(frame, classes=self.vehicle_classes, conf=self.conf, verbose=False)
        detections = []

        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            conf = float(result.conf[0])
            cls = int(result.cls[0])
            label = self.model.names[cls]

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "confidence": conf,
                "class": cls,
                "label": label
            })

        return detections

    def draw(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = f"{det['label']} {det['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame
from ultralytics import YOLO
import cv2

# Load pretrained model (auto downloads)
model = YOLO("yolov8n.pt")

# Test on your video
cap = cv2.VideoCapture("data/videos/test.mp4")

vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, classes=vehicle_classes, conf=0.5)
    annotated = results[0].plot()

    cv2.imshow("YOLOv8 Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
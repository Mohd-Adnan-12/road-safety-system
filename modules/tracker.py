import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from deep_sort_realtime.deepsort_tracker import DeepSort

class VehicleTracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)

    def update(self, detections, frame):
        deep_sort_input = []

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            w = x2 - x1
            h = y2 - y1
            conf = det["confidence"]
            deep_sort_input.append(([x1, y1, w, h], conf, det["label"]))

        tracks = self.tracker.update_tracks(deep_sort_input, frame=frame)

        tracked_vehicles = []
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            label = track.get_det_class()

            tracked_vehicles.append({
                "id": track_id,
                "bbox": (x1, y1, x2, y2),
                "label": label
            })

        return tracked_vehicles

    def draw(self, frame, tracked_vehicles):
        for vehicle in tracked_vehicles:
            x1, y1, x2, y2 = vehicle["bbox"]
            track_id = vehicle["id"]
            label = vehicle["label"]

            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 2)

            # Draw ID
            cv2.putText(frame, f"ID:{track_id} {label}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)

        return frame

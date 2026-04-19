import math

class AggressiveDrivingDetector:
    def __init__(self):
        self.vehicle_history = {}  # track_id -> list of center positions
        self.history_limit = 20    # frames to remember

    def get_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def get_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def update(self, tracked_vehicles):
        alerts = []

        for vehicle in tracked_vehicles:
            track_id = vehicle["id"]
            bbox = vehicle["bbox"]
            center = self.get_center(bbox)

            # Store history
            if track_id not in self.vehicle_history:
                self.vehicle_history[track_id] = []

            self.vehicle_history[track_id].append(center)

            # Keep only recent frames
            if len(self.vehicle_history[track_id]) > self.history_limit:
                self.vehicle_history[track_id].pop(0)

            history = self.vehicle_history[track_id]

            # Need at least 5 frames
            if len(history) < 5:
                continue

            # ---- Check 1: Sudden Lane Change ----
            x_positions = [p[0] for p in history]
            x_diff = max(x_positions) - min(x_positions)
            if x_diff > 80:
                alerts.append({
                    "id": track_id,
                    "type": "Sudden Lane Change",
                    "bbox": bbox,
                    "color": (0, 165, 255)  # Orange
                })

            # ---- Check 2: Abrupt Braking ----
            if len(history) >= 10:
                recent_speed = self.get_distance(history[-1], history[-5])
                prev_speed = self.get_distance(history[-6], history[-10])
                if prev_speed > 10 and recent_speed < 3:
                    alerts.append({
                        "id": track_id,
                        "type": "Abrupt Braking",
                        "bbox": bbox,
                        "color": (0, 0, 255)  # Red
                    })

            # ---- Check 3: Overspeeding ----
            if len(history) >= 2:
                speed = self.get_distance(history[-1], history[-2])
                if speed > 25:
                    alerts.append({
                        "id": track_id,
                        "type": "Overspeeding",
                        "bbox": bbox,
                        "color": (0, 0, 255)  # Red
                    })

        # ---- Check 4: Tailgating ----
        centers = [(v["id"], self.get_center(v["bbox"])) for v in tracked_vehicles]
        for i in range(len(centers)):
            for j in range(i + 1, len(centers)):
                dist = self.get_distance(centers[i][1], centers[j][1])
                if dist < 60:
                    alerts.append({
                        "id": centers[i][0],
                        "type": "Tailgating",
                        "bbox": tracked_vehicles[i]["bbox"],
                        "color": (255, 0, 0)  # Blue
                    })

        return alerts
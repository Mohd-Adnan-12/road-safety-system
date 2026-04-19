class WrongWayDetector:
    def __init__(self, expected_direction="down"):
        # expected_direction: "down" = vehicles should move downward in frame
        # change to "up", "left", "right" based on your video
        self.expected_direction = expected_direction
        self.vehicle_history = {}
        self.history_limit = 10

    def get_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def update(self, tracked_vehicles):
        alerts = []

        for vehicle in tracked_vehicles:
            track_id = vehicle["id"]
            bbox = vehicle["bbox"]
            center = self.get_center(bbox)

            if track_id not in self.vehicle_history:
                self.vehicle_history[track_id] = []

            self.vehicle_history[track_id].append(center)

            if len(self.vehicle_history[track_id]) > self.history_limit:
                self.vehicle_history[track_id].pop(0)

            history = self.vehicle_history[track_id]

            if len(history) < 5:
                continue

            # Calculate movement direction
            y_start = history[0][1]
            y_end = history[-1][1]
            x_start = history[0][0]
            x_end = history[-1][0]

            y_diff = y_end - y_start
            x_diff = x_end - x_start

            # Detect wrong way based on expected direction
            wrong_way = False

            if self.expected_direction == "down" and y_diff < -20:
                wrong_way = True
            elif self.expected_direction == "up" and y_diff > 20:
                wrong_way = True
            elif self.expected_direction == "right" and x_diff < -20:
                wrong_way = True
            elif self.expected_direction == "left" and x_diff > 20:
                wrong_way = True

            if wrong_way:
                alerts.append({
                    "id": track_id,
                    "type": "Wrong Way",
                    "bbox": bbox,
                    "color": (0, 0, 255)
                })

        return alerts

import csv
import os
import cv2
from datetime import datetime

class AlertLogger:
    def __init__(self, log_path="data/logs/incident_log.csv",
                 screenshot_path="data/screenshots/"):
        self.log_path = log_path
        self.screenshot_path = screenshot_path
        self.logged_ids = {}  # track_id -> last logged time

        # Create CSV with headers if not exists
        if not os.path.exists(log_path):
            with open(log_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "Vehicle ID",
                    "Alert Type", "Screenshot"
                ])

    def should_log(self, track_id, alert_type):
        key = f"{track_id}_{alert_type}"
        now = datetime.now()

        if key not in self.logged_ids:
            self.logged_ids[key] = now
            return True

        # Log same alert again only after 5 seconds
        diff = (now - self.logged_ids[key]).seconds
        if diff > 5:
            self.logged_ids[key] = now
            return True

        return False

    def log(self, frame, alerts):
        for alert in alerts:
            track_id = alert["id"]
            alert_type = alert["type"]

            if not self.should_log(track_id, alert_type):
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save screenshot
            filename = f"{alert_type.replace(' ', '_')}_{track_id}_{datetime.now().strftime('%H%M%S')}.jpg"
            filepath = os.path.join(self.screenshot_path, filename)
            cv2.imwrite(filepath, frame)

            # Write to CSV
            with open(self.log_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp, track_id,
                    alert_type, filename
                ])

            print(f"[ALERT] {timestamp} | ID:{track_id} | {alert_type}")
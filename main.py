from modules.detector import VehicleDetector
from modules.tracker import VehicleTracker
from modules.aggressive import AggressiveDrivingDetector
from modules.wrong_way import WrongWayDetector
from alerts.alert_logger import AlertLogger
from alerts.email_alert import EmailAlert
import cv2

# Initialize all modules
detector = VehicleDetector()
tracker = VehicleTracker()
aggressive = AggressiveDrivingDetector()
wrong_way = WrongWayDetector(expected_direction="down")
logger = AlertLogger()

# Initialize email alert
email_alert = EmailAlert(
    sender_email="mohammedadnan1285@gmail.com",       # your gmail
    sender_password="jzux nzoa zvzy shuf", # app password
    receiver_email="mohammedadnan1285@gmail.com"  # alert receiver
)

cap = cv2.VideoCapture("data/videos/test.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect
    detections = detector.detect(frame)

    # Track
    tracked_vehicles = tracker.update(detections, frame)

    # Aggressive detection
    aggressive_alerts = aggressive.update(tracked_vehicles)

    # Wrong way detection
    wrong_way_alerts = wrong_way.update(tracked_vehicles)

    # Combine all alerts
    all_alerts = aggressive_alerts + wrong_way_alerts

    # Log alerts + save screenshots
    logger.log(frame, all_alerts)

    # Send email alerts
    for alert in all_alerts:
        screenshot = f"data/screenshots/{alert['type'].replace(' ', '_')}_{alert['id']}.jpg"
        email_alert.send(
            alert_type=alert["type"],
            vehicle_id=alert["id"],
            screenshot_path=screenshot
        )

    # Draw tracked vehicles
    frame = tracker.draw(frame, tracked_vehicles)

    # Draw all alerts
    for alert in all_alerts:
        x1, y1, x2, y2 = alert["bbox"]
        color = alert["color"]
        label = f"! {alert['type']} ID:{alert['id']}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Stats
    cv2.putText(frame, f"Vehicles: {len(tracked_vehicles)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Alerts: {len(all_alerts)}", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Road Safety System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
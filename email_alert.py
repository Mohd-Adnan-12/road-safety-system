import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import os

class EmailAlert:
    def __init__(self, sender_email, sender_password, receiver_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
        self.last_sent = {}  # alert_type -> last sent time
        self.cooldown = 30   # seconds between same alert emails

    def should_send(self, alert_type):
        now = datetime.now()
        if alert_type not in self.last_sent:
            self.last_sent[alert_type] = now
            return True
        diff = (now - self.last_sent[alert_type]).seconds
        if diff > self.cooldown:
            self.last_sent[alert_type] = now
            return True
        return False

    def send(self, alert_type, vehicle_id, screenshot_path=None):
        if not self.should_send(alert_type):
            return

        try:
            # Create email
            msg = MIMEMultipart()
            msg["Subject"] = f"🚨 Road Safety Alert: {alert_type}"
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email

            # Email body
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            body = f"""
            Road Safety Alert Detected!

            Alert Type  : {alert_type}
            Vehicle ID  : {vehicle_id}
            Timestamp   : {timestamp}

            Please review the attached screenshot.

            -- Road Safety Monitoring System
            """

            msg.attach(MIMEText(body, "plain"))

            # Attach screenshot if exists
            if screenshot_path and os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=os.path.basename(screenshot_path)
                    )
                    msg.attach(img)

            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())

            print(f"[EMAIL SENT] {alert_type} | ID:{vehicle_id} | {timestamp}")

        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
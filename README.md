# 🚦 Real-Time Multi-Hazard Road Safety Monitoring System
## with Aggressive Driving Behavior Analysis Using YOLOv8

---

## 📌 About The Project

Road safety is one of the most critical challenges in modern transportation systems. Traditional traffic monitoring relies on manual surveillance which is slow, expensive, and error-prone. This project addresses that problem by building an **AI-powered, real-time road safety monitoring system** that automatically detects dangerous driving behaviors from CCTV or dashcam footage — without any human intervention.

Using **YOLOv8** for vehicle detection and **DeepSORT** for multi-object tracking, the system analyzes vehicle movement patterns over time to identify aggressive driving behaviors such as sudden lane changes, abrupt braking, overspeeding, and tailgating — along with wrong-way vehicle detection. Every violation is instantly logged, screenshot is captured, and an email alert is sent — all visualized on a live **Streamlit dashboard**.

---

## 🎯 What Problem Does It Solve?

- ❌ Manual traffic monitoring is slow and unreliable
- ❌ Existing systems only detect vehicles — not behavior
- ❌ No real-time alerting for dangerous driving
- ✅ This system detects, tracks, analyzes, alerts — all automatically in real-time

---

## 🚨 What The System Detects

### 🔵 Vehicle Detection & Tracking
- Detects cars, motorcycles, buses, and trucks
- Assigns a unique ID to each vehicle using DeepSORT
- Tracks every vehicle's movement across frames

### 🟠 Aggressive Driving Behaviors
| Behavior | How It Is Detected |
|---|---|
| **Sudden Lane Change** | Vehicle shifts horizontally too fast in short time |
| **Abrupt Braking** | Vehicle speed drops suddenly from high to near zero |
| **Overspeeding** | Vehicle moves too many pixels per frame beyond threshold |
| **Tailgating** | Two vehicles are detected too close to each other |

### 🔴 Wrong-Way Detection
- Identifies vehicles moving opposite to the normal traffic flow direction
- Based on historical movement analysis across frames

---

## ⚙️ How It Works

```
Video Input (CCTV / Dashcam)
        ↓
YOLOv8 — Detects all vehicles in each frame
        ↓
DeepSORT — Assigns unique ID and tracks each vehicle
        ↓
Behavior Analysis — Checks for aggressive driving patterns
        ↓
Wrong-Way Detection — Checks movement direction
        ↓
Alert System — Logs to CSV + saves screenshot + sends email
        ↓
Streamlit Dashboard — Displays live stats, charts, incidents
```

---

## 📊 Live Dashboard Features

- 📈 **Metric Cards** — Total alerts, vehicles tracked, most common violation
- 📊 **Bar Chart** — Alert type distribution
- 🥧 **Pie Chart** — Violation percentage breakdown
- 📋 **Incident Log Table** — Last 20 incidents with timestamps
- 📸 **Screenshot Gallery** — Last 6 violation snapshots
- ⚙️ **Auto Refresh** — Dashboard updates every few seconds

---

## 🏗️ Project Structure

```
road-safety-system/
│
├── main.py                      # Entry point — runs full pipeline
├── config.py                    # Settings and thresholds
├── requirements.txt             # All dependencies
├── README.md                    # Project documentation
│
├── modules/
│   ├── detector.py              # YOLOv8 vehicle detection
│   ├── tracker.py               # DeepSORT vehicle tracking
│   ├── aggressive.py            # Aggressive driving behavior detection
│   └── wrong_way.py             # Wrong-way vehicle detection
│
├── alerts/
│   ├── alert_logger.py          # Saves incidents to CSV + screenshots
│   └── email_alert.py          # Sends email alerts with screenshots
│
├── dashboard/
│   └── app.py                   # Streamlit live dashboard
│
├── models/
│   └── yolov8n.pt               # YOLOv8 pretrained model
│
└── data/
    ├── videos/                  # Input traffic video files
    ├── screenshots/             # Auto-saved violation snapshots
    └── logs/
        └── incident_log.csv     # All incidents logged here
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Vehicle Detection | YOLOv8 (Ultralytics) |
| Vehicle Tracking | DeepSORT |
| Video Processing | OpenCV |
| Behavior Analysis | Custom Python Logic |
| Dashboard UI | Streamlit |
| Charts | Plotly |
| Email Alerts | smtplib (Gmail SMTP) |
| Data Logging | Pandas + CSV |
| Language | Python 3.8+ |

---

## ⚙️ Installation & Setup

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/road-safety-system.git
cd road-safety-system
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add Your Traffic Video
```
Place your video inside: data/videos/test.mp4
```

### Step 5 — Configure Email Alerts
Open `main.py` and update:

email_alert = EmailAlert(
    sender_email="your@gmail.com",
    sender_password="xxxx xxxx xxxx xxxx",  # Gmail App Password
    receiver_email="receiver@gmail.com"
)
```

> **How to get Gmail App Password:**
> Go to myaccount.google.com/apppasswords → Generate password for Mail → Copy 16-digit password

---

## 🚀 Running The Project

### Terminal 1 — Run Detection System

python main.py


### Terminal 2 — Run Live Dashboard

streamlit run dashboard/app.py
```

Open browser at: **http://localhost:8501**

---

## 🎨 Alert Color Coding (On Video)

| Color | Violation Type |
|---|---|
| 🟠 Orange Box | Sudden Lane Change |
| 🔴 Red Box | Abrupt Braking / Overspeeding |
| 🔵 Blue Box | Tailgating |
| 🔴 Red Box | Wrong-Way Vehicle |

---

## 📦 Requirements

```
ultralytics
opencv-python
torch
torchvision
streamlit
deep-sort-realtime
plotly
pandas
pillow
numpy
```

---

## 📈 Performance

| Metric | Value |
|---|---|
| Detection Speed | ~35ms per frame |
| Model Used | YOLOv8n (nano) |
| Vehicle Classes | Car, Truck, Bus, Motorcycle |
| Processing Speed | ~28 FPS on CPU |

---

## 🎓 Project Information

| Field | Details |
|---|---|
| Project Title | Real-Time Multi-Hazard Road Safety Monitoring System with Aggressive Driving Behavior Analysis Using YOLOv8 |
| Domain | Computer Vision / Deep Learning |
| Institution | Vardhaman College of Engineering |
| Department | B.Tech CSE (AI & ML) |
| Academic Year | 2025-26 |

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ **If you found this project helpful, please give it a star on GitHub!**

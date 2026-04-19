import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from PIL import Image

# Page config
st.set_page_config(
    page_title="Road Safety Monitoring System",
    page_icon="🚦",
    layout="wide"
)

# Title
st.title("🚦 Real-Time Multi-Hazard Road Safety Monitoring System")
st.markdown("**AI-Powered Road Safety Dashboard using YOLOv8**")
st.divider()

# Paths
LOG_PATH = "data/logs/incident_log.csv"
SCREENSHOT_PATH = "data/screenshots/"

# ---- Sidebar ----
st.sidebar.title("⚙️ Settings")
auto_refresh = st.sidebar.toggle("Auto Refresh", value=True)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 2, 10, 3)
st.sidebar.divider()
st.sidebar.markdown("### 🎯 Alert Types")
st.sidebar.markdown("🟠 Sudden Lane Change")
st.sidebar.markdown("🔴 Abrupt Braking")
st.sidebar.markdown("🔴 Overspeeding")
st.sidebar.markdown("🔵 Tailgating")
st.sidebar.markdown("🔴 Wrong Way")

# ---- Load Data ----
def load_data():
    if os.path.exists(LOG_PATH):
        df = pd.read_csv(LOG_PATH)
        return df
    return pd.DataFrame(columns=[
        "Timestamp", "Vehicle ID", "Alert Type", "Screenshot"
    ])

# ---- Main Dashboard ----
def show_dashboard():
    df = load_data()

    # ---- Metric Cards ----
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🚨 Total Alerts", len(df))
    with col2:
        st.metric("🚗 Vehicles Tracked",
                  df["Vehicle ID"].nunique() if not df.empty else 0)
    with col3:
        most_common = df["Alert Type"].mode()[0] if not df.empty else "None"
        st.metric("⚠️ Most Common Alert", most_common)
    with col4:
        recent = df.tail(1)["Timestamp"].values[0] if not df.empty else "None"
        st.metric("🕐 Last Alert", recent)

    st.divider()

    # ---- Charts Row ----
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Alert Type Distribution")
        if not df.empty:
            alert_counts = df["Alert Type"].value_counts().reset_index()
            alert_counts.columns = ["Alert Type", "Count"]
            fig = px.bar(alert_counts, x="Alert Type", y="Count",
                        color="Alert Type",
                        color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No alerts detected yet")

    with col2:
        st.subheader("🥧 Alert Distribution")
        if not df.empty:
            fig2 = px.pie(df, names="Alert Type",
                         color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No alerts detected yet")

    st.divider()

    # ---- Recent Alerts Table ----
    st.subheader("📋 Recent Incident Log")
    if not df.empty:
        st.dataframe(
            df.tail(20).sort_index(ascending=False),
            use_container_width=True
        )
    else:
        st.info("No incidents logged yet")

    st.divider()

    # ---- Screenshots Gallery ----
    st.subheader("📸 Recent Violation Screenshots")
    screenshots = []

    if os.path.exists(SCREENSHOT_PATH):
        screenshots = sorted(
            [f for f in os.listdir(SCREENSHOT_PATH) if f.endswith(".jpg")],
            reverse=True
        )[:6]  # Show last 6

    if screenshots:
        cols = st.columns(3)
        for i, img_file in enumerate(screenshots):
            with cols[i % 3]:
                img = Image.open(os.path.join(SCREENSHOT_PATH, img_file))
                st.image(img, caption=img_file, use_column_width=True)
    else:
        st.info("No screenshots saved yet")

# ---- Run Dashboard ----
show_dashboard()

# Auto refresh
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

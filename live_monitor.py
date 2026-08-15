import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os
from streamlit_autorefresh import st_autorefresh
from src.mitigation_engine import get_mitigation_action  # Integration: Adaptive mitigation engine

# Auto refresh every 2 seconds for live stream simulation
st_autorefresh(interval=2000, key="live")

st.set_page_config(
    page_title="Live DDoS Monitoring",
    page_icon="🛡️",
    layout="wide"
)

# Load machine learning models
model = joblib.load("models/xgboost_ddos_model.pkl")
anomaly_model = joblib.load("models/anomaly_detector.pkl")

# Determine active target dataset: check if a file was uploaded in app.py
active_target_file = "data/active_target.parquet"
active_name_file = "data/active_target_name.txt"

if os.path.exists(active_target_file):
    dataset_path = active_target_file
    monitored_filename = "Uploaded Dataset"
    if os.path.exists(active_name_file):
        try:
            with open(active_name_file, "r", encoding="utf-8") as f:
                name_content = f.read().strip()
                if name_content:
                    monitored_filename = name_content
        except Exception:
            pass
    source_type = "Uploaded File"
else:
    dataset_path = "data/combined_dataset.parquet"
    monitored_filename = "combined_dataset.parquet"
    source_type = "Default Dataset"

# Load the target dataset
df = pd.read_parquet(dataset_path)

# Reset session pointer if the monitored file changes
if "current_monitored_file" not in st.session_state or st.session_state.current_monitored_file != monitored_filename:
    st.session_state.current_monitored_file = monitored_filename
    st.session_state.pointer = 0

st.title("🛡️ Simulated Live DDoS Monitoring")
st.info(f"📁 **Currently Monitoring File:** `{monitored_filename}` ({source_type}) | 📊 Total Records: {len(df):,}")

# Session pointer for batch streaming
if "pointer" not in st.session_state:
    st.session_state.pointer = 0

BATCH_SIZE = 100

start = st.session_state.pointer
end = start + BATCH_SIZE

batch = df.iloc[start:end]

if len(batch) == 0:
    st.success("🎉 Live Traffic Monitoring Completed for this Dataset!")
    if st.button("🔄 Restart Stream from Beginning"):
        st.session_state.pointer = 0
        st.rerun()
    st.stop()

st.session_state.pointer += BATCH_SIZE

# Remove Label column if present
X = batch.drop(
    "Label",
    axis=1,
    errors="ignore"
)

# XGBoost prediction
predictions = model.predict(X)
attack_count = int(predictions.sum())
Normal_count = len(predictions) - attack_count

# Isolation Forest anomaly prediction
anomaly_predictions = anomaly_model.predict(X)
anomaly_count = int((anomaly_predictions == -1).sum())

# Calculate composite Risk Score for current batch
risk_score = (
    (attack_count / len(X)) * 70
) + (
    (anomaly_count / len(X)) * 30
)

# Streamlit Metrics
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Current Batch Range",
        f"{start} - {end}"
    )

with c2:
    st.metric(
        "Attack Records",
        attack_count
    )

with c3:
    st.metric(
        "Normal Records",
        Normal_count
    )

with c4:
    st.metric(
        "Anomalies",
        anomaly_count
    )

# Detection Status
if attack_count > Normal_count:
    st.error("⚠️ DDoS Attack Detected in Current Batch")
else:
    st.success("✅ Normal Traffic in Current Batch")

# Risk Assessment
st.subheader("🛡️ Batch Risk Assessment")

st.progress(min(int(risk_score), 100))
st.write(f"Risk Score: {risk_score:.2f}%")

# Risk Level & Adaptive Mitigation Integration
if risk_score < 25:
    risk_level = "Low"
elif risk_score < 50:
    risk_level = "Medium"
elif risk_score < 75:
    risk_level = "High"
else:
    risk_level = "Critical"

mitigation_action, mitigation_desc, severity = get_mitigation_action(risk_level)

st.subheader("⚡ Adaptive Mitigation Response")
alert_msg = f"**Risk Level:** {risk_level} | **Recommended Action:** {mitigation_action}\n\n**Description:** {mitigation_desc}"

if risk_level == "Low":
    st.success(alert_msg)
elif risk_level == "Medium":
    st.warning(alert_msg)
else:
    st.error(alert_msg)

# Traffic Distribution Pie Chart
chart_df = pd.DataFrame({
    "Category": [
        "Attack",
        "Normal",
        "Anomaly"
    ],
    "Count": [
        attack_count,
        Normal_count,
        anomaly_count
    ]
})

fig = px.pie(
    chart_df,
    names="Category",
    values="Count",
    title="Live Traffic Batch Analysis"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# Preview Current Batch Traffic Records
st.subheader("📋 Current Batch Traffic Records")
st.dataframe(
    batch.head(20),
    width="stretch"
)
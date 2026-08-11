import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="live")

st.set_page_config(
    page_title="Live DDoS Monitoring",
    page_icon="🛡️",
    layout="wide"
)

# Load models
model = joblib.load(
    "models/xgboost_ddos_model.pkl"
)

anomaly_model = joblib.load(
    "models/anomaly_detector.pkl"
)

# Load dataset
df = pd.read_parquet(
    "data/combined_dataset.parquet"
)

st.title(
    "🛡️ Simulated Live DDoS Monitoring"
)

# Session pointer
if "pointer" not in st.session_state:
    st.session_state.pointer = 0

BATCH_SIZE = 100

start = st.session_state.pointer
end = start + BATCH_SIZE

batch = df.iloc[start:end]

if len(batch) == 0:
    st.success("Monitoring Completed")
    st.stop()

st.session_state.pointer += BATCH_SIZE

# Remove Label
X = batch.drop(
    "Label",
    axis=1,
    errors="ignore"
)

# XGBoost prediction
predictions = model.predict(X)

attack_count = int(predictions.sum())
benign_count = len(predictions) - attack_count

# Isolation Forest
anomaly_predictions = anomaly_model.predict(X)

anomaly_count = int(
    (anomaly_predictions == -1).sum()
)

# Risk score
risk_score = (
    (attack_count / len(X)) * 70
) + (
    (anomaly_count / len(X)) * 30
)

# Metrics
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Current Batch",
        f"{start} - {end}"
    )

with c2:
    st.metric(
        "Attack Records",
        attack_count
    )

with c3:
    st.metric(
        "Benign Records",
        benign_count
    )

with c4:
    st.metric(
        "Anomalies",
        anomaly_count
    )

# Status
if attack_count > benign_count:
    st.error(
        "⚠️ DDoS Attack Detected"
    )
else:
    st.success(
        "✅ Normal Traffic"
    )

# Risk
st.subheader("Risk Score")

st.progress(
    min(int(risk_score), 100)
)

st.write(
    f"Risk Score: {risk_score:.2f}%"
)

# Pie chart
chart_df = pd.DataFrame({
    "Category": [
        "Attack",
        "Benign",
        "Anomaly"
    ],
    "Count": [
        attack_count,
        benign_count,
        anomaly_count
    ]
})

fig = px.pie(
    chart_df,
    names="Category",
    values="Count",
    title="Live Traffic Analysis"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# Live records
st.subheader(
    "Current Traffic Records"
)

st.dataframe(
    batch.head(20),
    width="stretch"
)
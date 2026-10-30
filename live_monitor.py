import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit_autorefresh import st_autorefresh
from src.mitigation_engine import get_mitigation_action

# Auto refresh every 2 seconds for live stream simulation
st_autorefresh(interval=2000, key="live")

st.set_page_config(
    page_title="Live DDoS Radar · Stream Simulation",
    page_icon="📡",
    layout="wide"
)

# ==============================================================================
# Custom CSS Design System (Cyberpunk Dark UI)
# ==============================================================================
LIVE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-card: rgba(18, 26, 43, 0.75);
    --border-color: rgba(0, 242, 254, 0.15);
    --border-glow: rgba(0, 242, 254, 0.4);
    --cyan-glow: #00f2fe;
    --blue-electric: #4facfe;
    --danger-red: #ff3366;
    --warning-amber: #ffb800;
    --safe-green: #00f5a0;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(0, 242, 254, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 51, 102, 0.04) 0%, transparent 40%),
                #0a0e17;
}

.soc-hero {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(16px);
    position: relative;
}

.soc-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #ff3366, #00f2fe, transparent);
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 51, 102, 0.12);
    color: #ff3366;
    border: 1px solid rgba(255, 51, 102, 0.3);
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.pulse-dot-red {
    width: 8px;
    height: 8px;
    background-color: #ff3366;
    border-radius: 50%;
    box-shadow: 0 0 10px #ff3366;
    animation: livepulse 1.5s infinite;
}

@keyframes livepulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 51, 102, 0.8); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 9px rgba(255, 51, 102, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 51, 102, 0); }
}

.soc-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}

.soc-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-glow);
}

.soc-card-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
}

.soc-card-value {
    font-size: 30px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    margin: 6px 0 2px 0;
}

.stButton>button {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    color: #050b14;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
}
</style>
"""
st.markdown(LIVE_CSS, unsafe_allow_html=True)

# Load machine learning models
@st.cache_resource(show_spinner=False)
def load_models():
    m = joblib.load("models/xgboost_ddos_model.pkl")
    a = joblib.load("models/anomaly_detector.pkl")
    return m, a

model, anomaly_model = load_models()

# Determine active target dataset
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
    source_type = "Active Target Ingestion"
else:
    dataset_path = "data/combined_dataset.parquet"
    monitored_filename = "combined_dataset.parquet"
    source_type = "Default Multi-Vector Benchmark"

df = pd.read_parquet(dataset_path)

if "current_monitored_file" not in st.session_state or st.session_state.current_monitored_file != monitored_filename:
    st.session_state.current_monitored_file = monitored_filename
    st.session_state.pointer = 0

if "pointer" not in st.session_state:
    st.session_state.pointer = 0

BATCH_SIZE = 100
start = st.session_state.pointer
end = start + BATCH_SIZE
batch = df.iloc[start:end]

# Hero Banner
st.markdown(f"""
    <div class="soc-hero">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <h1 style="margin: 0; font-size: 26px; font-weight: 800; color: #fff;">
                    📡 Simulated Real-Time DDoS Packet Stream
                </h1>
                <p style="margin: 5px 0 0 0; font-size: 13px; color: #94a3b8;">
                    Monitoring Target: <code style="color: #00f2fe; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px;">{monitored_filename}</code> &bull; {source_type} &bull; Total Available Flows: {len(df):,}
                </p>
            </div>
            <div class="live-indicator">
                <span class="pulse-dot-red"></span>
                <span>STREAM REFRESH 2s</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

if len(batch) == 0:
    st.success("🎉 Stream completed for the current dataset!")
    if st.button("🔄 Restart Stream from Offset 0"):
        st.session_state.pointer = 0
        st.rerun()
    st.stop()

st.session_state.pointer += BATCH_SIZE

# Run Inference
X = batch.drop("Label", axis=1, errors="ignore")
predictions = model.predict(X)
attack_count = int(predictions.sum())
Normal_count = len(predictions) - attack_count

anomaly_predictions = anomaly_model.predict(X)
anomaly_count = int((anomaly_predictions == -1).sum())

risk_score = ((attack_count / len(X)) * 70) + ((anomaly_count / len(X)) * 30)
risk_score = min(float(risk_score), 100.0)

if risk_score < 25:
    risk_level = "Low"
    accent_color = "#00f5a0"
    status_icon = "🟢"
elif risk_score < 50:
    risk_level = "Medium"
    accent_color = "#ffb800"
    status_icon = "🟡"
elif risk_score < 75:
    risk_level = "High"
    accent_color = "#ff7800"
    status_icon = "🟠"
else:
    risk_level = "Critical"
    accent_color = "#ff3366"
    status_icon = "🔴"

mitigation_action, mitigation_desc, severity = get_mitigation_action(risk_level)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class="soc-card">
            <div class="soc-card-label">Batch Packet Window</div>
            <div class="soc-card-value" style="color: #4facfe;">{start} - {end}</div>
            <div style="font-size: 11px; color: #64748b;">Progress: {(end/len(df))*100:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="soc-card" style="border-left: 3px solid #ff3366;">
            <div class="soc-card-label">Detected Attacks</div>
            <div class="soc-card-value" style="color: #ff3366;">{attack_count}</div>
            <div style="font-size: 11px; color: #ff3366;">{(attack_count/len(X))*100:.0f}% of batch</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="soc-card" style="border-left: 3px solid #00f5a0;">
            <div class="soc-card-label">Normal Packets</div>
            <div class="soc-card-value" style="color: #00f5a0;">{Normal_count}</div>
            <div style="font-size: 11px; color: #00f5a0;">{(Normal_count/len(X))*100:.0f}% of batch</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class="soc-card" style="border-left: 3px solid #ffb800;">
            <div class="soc-card-label">Anomalies</div>
            <div class="soc-card-value" style="color: #ffb800;">{anomaly_count}</div>
            <div style="font-size: 11px; color: #ffb800;">iForest Zero-Day Spikes</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# Mitigation & Live Visualizer
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 14px; padding: 20px; height: 100%;">
            <div style="font-size: 12px; color: {accent_color}; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                {status_icon} Incident Threat: {risk_level.upper()} RISK ({risk_score:.1f}%)
            </div>
            <h3 style="margin: 6px 0 10px 0; color: #fff; font-size: 20px;">
                {mitigation_action}
            </h3>
            <p style="color: #cbd5e1; font-size: 13px; line-height: 1.5; margin-bottom: 15px;">
                {mitigation_desc}
            </p>
            <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; font-size: 11px; color: #64748b;">
                Autonomous mitigation triggers dispatched dynamically based on batch threat density.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    chart_df = pd.DataFrame({
        "Category": ["Attack", "Normal", "Anomaly"],
        "Count": [attack_count, Normal_count, anomaly_count]
    })
    donut = go.Figure(data=[go.Pie(
        labels=chart_df["Category"],
        values=chart_df["Count"],
        hole=0.6,
        marker=dict(colors=["#ff3366", "#00f5a0", "#ffb800"], line=dict(color='#0a0e17', width=2))
    )])
    donut.update_layout(
        title=dict(text="<b>Batch Composition</b>", font=dict(color="#fff", size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
        margin=dict(l=10, r=10, t=35, b=10),
        height=240,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(donut, use_container_width=True)

# Batch Records Table
with st.expander("📋 Inspect Current Batch Records", expanded=False):
    st.dataframe(batch.head(20), use_container_width=True)
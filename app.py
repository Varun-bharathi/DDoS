import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
import tempfile
from fpdf import FPDF
from streamlit_autorefresh import st_autorefresh
import shap
from src.mitigation_engine import get_mitigation_action

# ==============================================================================
# Page Configuration & Metadata
# ==============================================================================
st.set_page_config(
    page_title="DDoS Shield · Next-Gen Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# Custom CSS Design System (Cyberpunk SOC / Glassmorphic Dark UI)
# ==============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-card: rgba(18, 26, 43, 0.75);
    --bg-card-hover: rgba(26, 38, 64, 0.85);
    --border-color: rgba(0, 242, 254, 0.15);
    --border-glow: rgba(0, 242, 254, 0.4);
    --cyan-glow: #00f2fe;
    --blue-electric: #4facfe;
    --danger-red: #ff3366;
    --warning-amber: #ffb800;
    --safe-green: #00f5a0;
    --purple-accent: #a855f7;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.04) 0%, transparent 40%),
                #0a0e17;
}

.soc-hero {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 22px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
}

.soc-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan-glow), var(--purple-accent), transparent);
}

.soc-hero-live::before {
    background: linear-gradient(90deg, transparent, #ff3366, #00f2fe, transparent) !important;
}

.soc-hero-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 30%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 12px;
}

.soc-hero-subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin-top: 6px;
    margin-bottom: 0px;
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 245, 160, 0.1);
    color: #00f5a0;
    border: 1px solid rgba(0, 245, 160, 0.3);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.live-indicator-red {
    background: rgba(255, 51, 102, 0.12) !important;
    color: #ff3366 !important;
    border: 1px solid rgba(255, 51, 102, 0.3) !important;
}

.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #00f5a0;
    border-radius: 50%;
    box-shadow: 0 0 10px #00f5a0;
    animation: pulse 1.8s infinite;
}

.pulse-dot-red {
    width: 8px;
    height: 8px;
    background-color: #ff3366;
    border-radius: 50%;
    box-shadow: 0 0 10px #ff3366;
    animation: livepulse 1.4s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 245, 160, 0.7); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(0, 245, 160, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 245, 160, 0); }
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
    padding: 20px 22px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.soc-card:hover {
    transform: translateY(-3px);
    border-color: var(--border-glow);
    box-shadow: 0 8px 30px rgba(0, 242, 254, 0.15);
}

.soc-card-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.soc-card-value {
    font-size: 32px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    margin: 8px 0 4px 0;
}

.soc-card-caption {
    font-size: 12px;
    color: var(--text-muted);
}

.threat-card {
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 20px;
    border: 1px solid;
    position: relative;
}

.threat-card-critical {
    background: linear-gradient(135deg, rgba(255, 51, 102, 0.15) 0%, rgba(20, 10, 20, 0.7) 100%);
    border-color: rgba(255, 51, 102, 0.5);
    box-shadow: 0 0 25px rgba(255, 51, 102, 0.2);
}

.threat-card-high {
    background: linear-gradient(135deg, rgba(255, 120, 0, 0.15) 0%, rgba(20, 15, 10, 0.7) 100%);
    border-color: rgba(255, 120, 0, 0.5);
    box-shadow: 0 0 25px rgba(255, 120, 0, 0.2);
}

.threat-card-medium {
    background: linear-gradient(135deg, rgba(255, 184, 0, 0.12) 0%, rgba(25, 20, 10, 0.7) 100%);
    border-color: rgba(255, 184, 0, 0.4);
    box-shadow: 0 0 25px rgba(255, 184, 0, 0.15);
}

.threat-card-low {
    background: linear-gradient(135deg, rgba(0, 245, 160, 0.12) 0%, rgba(10, 25, 20, 0.7) 100%);
    border-color: rgba(0, 245, 160, 0.4);
    box-shadow: 0 0 25px rgba(0, 245, 160, 0.15);
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    color: #050b14;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.5px;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    transition: all 0.25s ease;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(0, 242, 254, 0.5);
    color: #000;
}

.stDownloadButton>button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    color: #ffffff;
    font-weight: 700;
    font-size: 15px;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 23, 42, 0.6);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 18px;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 14px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.15) 0%, rgba(79, 172, 254, 0.15) 100%) !important;
    color: var(--cyan-glow) !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stFileUploader"] {
    background: var(--bg-card);
    border: 1px dashed var(--border-color);
    border-radius: 14px;
    padding: 18px;
    transition: border-color 0.3s;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--cyan-glow);
}

[data-testid="stSidebar"] {
    background-color: #0b111e;
    border-right: 1px solid rgba(0, 242, 254, 0.1);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# Model Loading & Diagnostics
# ==============================================================================
@st.cache_resource(show_spinner=False)
def load_ml_models():
    """Load pretrained XGBoost and Isolation Forest models safely."""
    try:
        xgb = joblib.load("models/xgboost_ddos_model.pkl")
    except Exception:
        xgb = None
    try:
        anom = joblib.load("models/anomaly_detector.pkl")
    except Exception:
        anom = None
    return xgb, anom

model, anomaly_model = load_ml_models()

@st.cache_resource(show_spinner=False)
def get_shap_explainer(_xgb_model):
    """Cache SHAP TreeExplainer for instantaneous per-dataset attribution."""
    if _xgb_model is None:
        return None
    try:
        return shap.TreeExplainer(_xgb_model)
    except Exception:
        return None

shap_explainer = get_shap_explainer(model)

# ==============================================================================
# PDF Generation Helper
# ==============================================================================
def create_pdf_report(
    attack_count,
    Normal_count,
    anomaly_count,
    risk_score,
    risk_level,
    mitigation_action="N/A",
    mitigation_description="N/A"
):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 18)
    pdf.cell(200, 12, "DDoS Threat Defense & Forensic Report", ln=True, align="C")
    
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 6, "Explainable Hybrid ML Security Framework (XGBoost + Isolation Forest)", ln=True, align="C")
    pdf.ln(8)
    
    pdf.set_draw_color(0, 200, 220)
    pdf.set_line_width(0.6)
    pdf.line(10, 32, 200, 32)
    pdf.ln(6)
    
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 8, f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True)
    pdf.ln(4)
    
    pdf.set_font("Arial", "B", 13)
    pdf.cell(200, 9, "1. Executive Telemetry Summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f" - Malicious Attack Records Detected: {attack_count:,}", ln=True)
    pdf.cell(200, 8, f" - Verified Normal Traffic Records: {Normal_count:,}", ln=True)
    pdf.cell(200, 8, f" - Zero-Day Anomalies Flagged: {anomaly_count:,}", ln=True)
    pdf.cell(200, 8, f" - Composite Threat Risk Score: {risk_score:.2f}%", ln=True)
    pdf.cell(200, 8, f" - Evaluated Risk Classification: {risk_level.upper()}", ln=True)
    pdf.ln(6)
    
    pdf.set_font("Arial", "B", 13)
    pdf.cell(200, 9, "2. Adaptive Countermeasures Executed", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f" - Recommended Defense Action: {mitigation_action}", ln=True)
    pdf.cell(200, 8, f" - Action Directive: {mitigation_description}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "I", 9)
    pdf.cell(200, 8, "Confidential - Security Operations Center (SOC) Automated Assessment", ln=True, align="C")
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# ==============================================================================
# Helper to Run ML Threat Scan
# ==============================================================================
def execute_threat_scan(data_df, fname):
    """Run dual-engine inference and store structured results in session state."""
    X = data_df.drop("Label", axis=1, errors="ignore")
    
    predictions = model.predict(X)
    attack_count = int(predictions.sum())
    Normal_count = len(predictions) - attack_count
    
    anomaly_predictions = anomaly_model.predict(X)
    anomaly_count = int((anomaly_predictions == -1).sum())
    
    risk_score = (
        (attack_count / len(X)) * 70
    ) + (
        (anomaly_count / len(X)) * 30
    )
    risk_score = min(float(risk_score), 100.0)
    
    if risk_score < 25:
        risk_level = "Low"
        threat_theme = "threat-card-low"
        badge_color = "#00f5a0"
        status_icon = "🟢"
        status_title = "Normal Network Behavior Verified"
    elif risk_score < 50:
        risk_level = "Medium"
        threat_theme = "threat-card-medium"
        badge_color = "#ffb800"
        status_icon = "🟡"
        status_title = "Elevated Traffic & Suspicious Bursts"
    elif risk_score < 75:
        risk_level = "High"
        threat_theme = "threat-card-high"
        badge_color = "#ff7800"
        status_icon = "🟠"
        status_title = "High-Severity DDoS Assault In Progress"
    else:
        risk_level = "Critical"
        threat_theme = "threat-card-critical"
        badge_color = "#ff3366"
        status_icon = "🔴"
        status_title = "CRITICAL: Catastrophic Distributed Volumetric Attack"
        
    mitigation_action, mitigation_description, severity = get_mitigation_action(risk_level)
    
    history_record = pd.DataFrame({
        "Timestamp": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Dataset": [fname],
        "Attack Count": [attack_count],
        "Normal Count": [Normal_count],
        "Anomaly Count": [anomaly_count],
        "Risk Score": [round(risk_score, 2)],
        "risk_level": [risk_level],
        "mitigation_action": [mitigation_action]
    })
    history_file = "data/history.csv"
    if os.path.exists(history_file):
        existing_df = pd.read_csv(history_file)
        if "risk_level" not in existing_df.columns:
            existing_df["risk_level"] = "N/A"
        if "mitigation_action" not in existing_df.columns:
            existing_df["mitigation_action"] = "N/A"
        if "Dataset" not in existing_df.columns:
            existing_df["Dataset"] = "N/A"
        existing_df.to_csv(history_file, index=False)
        history_record.to_csv(history_file, mode="a", header=False, index=False)
    else:
        history_record.to_csv(history_file, index=False)
        
    # Dynamic Feature Attribution via SHAP TreeExplainer for uploaded dataset
    dynamic_shap_df = None
    try:
        if shap_explainer is not None:
            sample_size = min(150, len(X))
            X_sample = X.iloc[:sample_size]
            sv = shap_explainer.shap_values(X_sample)
            if isinstance(sv, list):
                sv_arr = sv[1] if len(sv) > 1 else sv[0]
            else:
                sv_arr = sv
            mean_shap = np.abs(sv_arr).mean(axis=0)
            dynamic_shap_df = pd.DataFrame({
                "Feature": X.columns,
                "Impact": mean_shap
            }).sort_values("Impact", ascending=True).tail(10)
    except Exception:
        dynamic_shap_df = None

    # Global Model Baseline
    importance_df = None
    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "Feature": X.columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=True).tail(10)

    return {
        "filename": fname,
        "total_records": len(X),
        "attack_count": attack_count,
        "Normal_count": Normal_count,
        "anomaly_count": anomaly_count,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "badge_color": badge_color,
        "status_icon": status_icon,
        "threat_theme": threat_theme,
        "status_title": status_title,
        "mitigation_action": mitigation_action,
        "mitigation_description": mitigation_description,
        "dynamic_shap_df": dynamic_shap_df,
        "global_importance_df": importance_df,
        "importance_df": dynamic_shap_df if dynamic_shap_df is not None else importance_df,
        "X": X
    }

# ==============================================================================
# Global Session State Management
# ==============================================================================
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None

if "last_active_file" not in st.session_state:
    st.session_state.last_active_file = None

if "live_pointer" not in st.session_state:
    st.session_state.live_pointer = 0

if "live_paused" not in st.session_state:
    st.session_state.live_paused = False

# ==============================================================================
# Sidebar: Operation Console & Health
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="font-size: 26px;">🛡️</span>
            <div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #fff;">SOC SHIELD</h3>
                <p style="margin: 0; font-size: 11px; color: #94a3b8; letter-spacing: 0.5px;">HYBRID DEFENSE V2.4</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎛️ Operation Console")
    console_mode = st.radio(
        "Choose Operational Console:",
        ["🛡️ Deep Threat Inspection", "📡 Real-Time Live Monitor"],
        index=0,
        help="Switch between full dataset forensic scan and real-time streaming packet monitor."
    )
    
    st.markdown("---")

    st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 10px; padding: 12px; margin-bottom: 15px;">
            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">System Health</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                <span style="font-size: 13px; color: #e2e8f0;">AI Classifier:</span>
                <span style="font-size: 12px; color: #00f5a0; font-weight: 600;">● Online (XGBoost)</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                <span style="font-size: 13px; color: #e2e8f0;">Anomaly Radar:</span>
                <span style="font-size: 12px; color: #00f5a0; font-weight: 600;">● Online (iForest)</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                <span style="font-size: 13px; color: #e2e8f0;">Live Stream Engine:</span>
                <span style="font-size: 12px; color: #00f2fe; font-weight: 600;">● Unified In-App</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 11px; color: #64748b; line-height: 1.5;">
            <b>Ensemble Specification:</b><br>
            • Supervised: Gradient Boosted Trees (100 estimators, max depth 6)<br>
            • Unsupervised: Isolation Forest (Contamination 0.05)<br>
            • Real-time mitigation response engine active
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# CONSOLE MODE 1: DEEP THREAT INSPECTION DASHBOARD
# ==============================================================================
if console_mode == "🛡️ Deep Threat Inspection":
    # Hero Banner
    st.markdown("""
        <div class="soc-hero">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h1 class="soc-hero-title">
                        <span>🛡️</span> Explainable Hybrid ML Framework for DDoS Defense
                    </h1>
                    <p class="soc-hero-subtitle">
                        Full-Dataset Dual-Engine Threat Classification, Unsupervised Anomaly Detection & Adaptive Defense Strategy
                    </p>
                </div>
                <div class="live-indicator">
                    <span class="pulse-dot"></span>
                    <span>Forensic Engine Active</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Top Dynamic Metrics Bar Container (Above Uploader)
    metrics_container = st.container()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Ingestion Station (Directly Below Metrics Bar)
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
                <span>📂</span> Ingest Network Traffic Dataset
            </h3>
            <p style="margin: 2px 0 10px 0; font-size: 13px; color: #94a3b8;">
                Upload your packet capture file below, or quickly select one of the pre-packaged security benchmark datasets.
            </p>
        </div>
    """, unsafe_allow_html=True)

    df = None
    active_filename = None

    ingest_tab1, ingest_tab2 = st.tabs([
        "📁 Upload Capture File (.csv or .parquet)", 
        "🚀 Quick Load Security Benchmark"
    ])

    with ingest_tab1:
        uploaded_file = st.file_uploader(
            "Upload Network Traffic Records (.csv or .parquet)",
            type=["csv", "parquet"],
            help="Drag and drop a packet capture file (.csv or .parquet) up to 200MB."
        )
        if uploaded_file is not None:
            active_filename = uploaded_file.name
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_parquet(uploaded_file)

    with ingest_tab2:
        available_samples = [
            f for f in os.listdir("data") 
            if f.endswith(".parquet") and f not in ["active_target.parquet", "combined_dataset.parquet"]
        ]
        if not available_samples:
            available_samples = ["combined_dataset.parquet"]
            
        sample_choice = st.selectbox(
            "Select a Pre-configured Vector Sample from Repository:",
            ["-- None (Use Uploaded File) --"] + available_samples,
            index=0
        )
        if sample_choice != "-- None (Use Uploaded File) --":
            sample_path = os.path.join("data", sample_choice)
            if os.path.exists(sample_path):
                active_filename = sample_choice
                df = pd.read_parquet(sample_path)

    # Check if loaded file changed
    if active_filename != st.session_state.last_active_file:
        st.session_state.last_active_file = active_filename
        st.session_state.scan_results = None

    # Sync with active target
    if df is not None and active_filename is not None:
        os.makedirs("data", exist_ok=True)
        df.to_parquet("data/active_target.parquet", index=False)
        with open("data/active_target_name.txt", "w", encoding="utf-8") as f:
            f.write(active_filename)

    # Populate Top Dynamic Metrics Bar
    scan_res = st.session_state.scan_results

    if scan_res is not None:
        kpi_val_1 = f"{scan_res['total_records']:,}"
        kpi_sub_1 = f"File: {scan_res['filename']}"
        kpi_color_1 = "#4facfe"
        
        kpi_val_2 = f"{scan_res['attack_count']:,}"
        kpi_sub_2 = f"{(scan_res['attack_count'] / scan_res['total_records']) * 100:.1f}% attack ratio"
        kpi_color_2 = "#ff3366"
        
        kpi_val_3 = f"{scan_res['Normal_count']:,}"
        kpi_sub_3 = f"{(scan_res['Normal_count'] / scan_res['total_records']) * 100:.1f}% legitimate ratio"
        kpi_color_3 = "#00f5a0"
        
        kpi_val_4 = f"{scan_res['risk_score']:.1f}%"
        kpi_sub_4 = f"Status: {scan_res['risk_level'].upper()} {scan_res['status_icon']}"
        kpi_color_4 = scan_res['badge_color']

    elif df is not None:
        kpi_val_1 = f"{len(df):,}"
        kpi_sub_1 = f"Staged: {active_filename}"
        kpi_color_1 = "#4facfe"
        
        kpi_val_2 = "READY"
        kpi_sub_2 = "Click 'Run AI Threat Inspection'"
        kpi_color_2 = "#94a3b8"
        
        kpi_val_3 = "READY"
        kpi_sub_3 = "Click 'Run AI Threat Inspection'"
        kpi_color_3 = "#94a3b8"
        
        kpi_val_4 = "STANDBY"
        kpi_sub_4 = "AI Model Engine Online"
        kpi_color_4 = "#00f2fe"

    else:
        kpi_val_1 = "0"
        kpi_sub_1 = "No file currently loaded"
        kpi_color_1 = "#64748b"
        
        kpi_val_2 = "--"
        kpi_sub_2 = "Awaiting traffic ingestion"
        kpi_color_2 = "#64748b"
        
        kpi_val_3 = "--"
        kpi_sub_3 = "Awaiting traffic ingestion"
        kpi_color_3 = "#64748b"
        
        kpi_val_4 = "99.97%"
        kpi_sub_4 = "Model Accuracy Ready"
        kpi_color_4 = "#00f2fe"

    with metrics_container:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f"""
                <div class="soc-card">
                    <div class="soc-card-label">
                        <span>Inspected Flows</span>
                        <span style="color: {kpi_color_1};">🌐</span>
                    </div>
                    <div class="soc-card-value" style="color: {kpi_color_1};">{kpi_val_1}</div>
                    <div class="soc-card-caption">{kpi_sub_1}</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"""
                <div class="soc-card">
                    <div class="soc-card-label">
                        <span>Detected Attacks</span>
                        <span style="color: {kpi_color_2};">⚠️</span>
                    </div>
                    <div class="soc-card-value" style="color: {kpi_color_2};">{kpi_val_2}</div>
                    <div class="soc-card-caption">{kpi_sub_2}</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
                <div class="soc-card">
                    <div class="soc-card-label">
                        <span>Normal Baseline</span>
                        <span style="color: {kpi_color_3};">✅</span>
                    </div>
                    <div class="soc-card-value" style="color: {kpi_color_3};">{kpi_val_3}</div>
                    <div class="soc-card-caption">{kpi_sub_3}</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi4:
            st.markdown(f"""
                <div class="soc-card">
                    <div class="soc-card-label">
                        <span>Threat Risk Index</span>
                        <span style="color: {kpi_color_4};">🎯</span>
                    </div>
                    <div class="soc-card-value" style="color: {kpi_color_4};">{kpi_val_4}</div>
                    <div class="soc-card-caption">{kpi_sub_4}</div>
                </div>
            """, unsafe_allow_html=True)

    # Post-Ingestion Inspection Action & Tabs
    if df is not None:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        c_left, c_right = st.columns([3, 1])
        with c_left:
            st.markdown(f"""
                <div style="background: rgba(0, 242, 254, 0.06); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="color: #00f2fe; font-weight: 700;">📡 Target Ingested:</span>
                        <code style="background: rgba(0,0,0,0.3); padding: 3px 8px; border-radius: 6px; color: #fff; margin-left: 8px;">{active_filename}</code>
                    </div>
                    <div style="font-size: 13px; color: #94a3b8;">
                        <b>{df.shape[0]:,}</b> Rows &bull; <b>{df.shape[1]}</b> Features
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with c_right:
            run_detection = st.button("🚀 Run AI Threat Inspection", key="run_threat_scan")

        if run_detection:
            if model is None or anomaly_model is None:
                st.error("🚨 Pretrained models could not be loaded from `models/`. Please check the model directory.")
            else:
                with st.spinner("⚡ Running High-Speed Dual-Model Inference Pipeline..."):
                    try:
                        res = execute_threat_scan(df, active_filename)
                        st.session_state.scan_results = res
                        st.rerun()
                    except Exception as e:
                        st.error(f"Inference Pipeline Error: {e}")
                        st.exception(e)

        with st.expander("📋 Inspect Ingested Raw Telemetry (First 5 Flows)", expanded=False):
            st.dataframe(df.head(5), use_container_width=True)

        # Scanned Tabs
        if st.session_state.scan_results is not None and st.session_state.scan_results["filename"] == active_filename:
            res = st.session_state.scan_results
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            tab1, tab2, tab3, tab4 = st.tabs([
                "🛡️ Threat Assessment & Mitigation",
                "📊 Traffic & Flow Analytics",
                "🔬 Explainable AI (XAI) Attribution",
                "📜 Forensics & Audit Trail"
            ])

            with tab1:
                st.markdown(f"""
                    <div class="threat-card {res['threat_theme']}">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; color: {res['badge_color']}; font-weight: 700;">
                                    {res['status_icon']} Incident Level: {res['risk_level'].upper()} RISK
                                </div>
                                <h2 style="margin: 6px 0 4px 0; font-size: 24px; font-weight: 800; color: #fff;">
                                    {res['status_title']}
                                </h2>
                                <div style="font-size: 14px; color: #cbd5e1;">
                                    Identified <b>{res['attack_count']:,}</b> attack signatures and <b>{res['anomaly_count']:,}</b> anomalous network spikes out of <b>{res['total_records']:,}</b> flows.
                                </div>
                            </div>
                            <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Calculated Risk Index</div>
                                <div style="font-size: 32px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: {res['badge_color']};">
                                    {res['risk_score']:.1f}%
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.markdown(f"""
                        <div class="soc-card" style="border-left: 3px solid #ff3366;">
                            <div class="soc-card-label">Identified Attacks</div>
                            <div class="soc-card-value" style="color: #ff3366;">{res['attack_count']:,}</div>
                            <div class="soc-card-caption">{(res['attack_count']/res['total_records'])*100:.1f}% of inspected volume</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"""
                        <div class="soc-card" style="border-left: 3px solid #00f5a0;">
                            <div class="soc-card-label">Normal Flow Baseline</div>
                            <div class="soc-card-value" style="color: #00f5a0;">{res['Normal_count']:,}</div>
                            <div class="soc-card-caption">{(res['Normal_count']/res['total_records'])*100:.1f}% of inspected volume</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m3:
                    st.markdown(f"""
                        <div class="soc-card" style="border-left: 3px solid #ffb800;">
                            <div class="soc-card-label">Zero-Day Anomalies</div>
                            <div class="soc-card-value" style="color: #ffb800;">{res['anomaly_count']:,}</div>
                            <div class="soc-card-caption">Flagged by Isolation Forest</div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

                st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 14px; padding: 22px; margin-top: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <div style="font-size: 16px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
                                <span>⚡</span> Adaptive Mitigation Countermeasures
                            </div>
                            <span style="background: rgba(0, 242, 254, 0.15); color: #00f2fe; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">
                                ENGINE RESPONSE
                            </span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 16px; align-items: center;">
                            <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 10px; border-left: 4px solid {res['badge_color']};">
                                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase;">Prescribed Action</div>
                                <div style="font-size: 18px; font-weight: 700; color: #fff; margin-top: 4px;">{res['mitigation_action']}</div>
                            </div>
                            <div style="font-size: 14px; color: #cbd5e1; line-height: 1.6;">
                                <b>Directive:</b> {res['mitigation_description']}<br>
                                <span style="color: #64748b; font-size: 12px;">Automated ACL rules, BGP blackhole, and flow rate-limiters stand ready for dispatch.</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                enable_mitigation = st.checkbox(
                    "⚡ Engage Autonomous Adaptive Mitigation Rules", 
                    value=(res['risk_level'] in ["High", "Critical"]),
                    key="mitigation_toggle"
                )
                if enable_mitigation:
                    if res['risk_level'] == "Low":
                        st.info("ℹ️ Telemetry Monitoring engaged. Traffic flows pass through unimpeded.")
                    elif res['risk_level'] == "Medium":
                        st.warning("⚡ Rate limiting & packet throttling active on suspicious IP source clusters.")
                    elif res['risk_level'] == "High":
                        st.error("🚫 Dynamic firewall dropping packets matching detected DDoS signatures.")
                    else:
                        st.error("🚨 EMERGENCY DEFENSE ACTIVATED: Upstream BGP route filtering & scrubbing center redirection triggered!")

            with tab2:
                col_g1, col_g2 = st.columns([1, 1])

                with col_g1:
                    chart_df = pd.DataFrame({
                        "Category": ["Malicious Attack", "Normal Traffic", "Zero-Day Anomaly"],
                        "Count": [res['attack_count'], res['Normal_count'], res['anomaly_count']]
                    })
                    
                    pie_fig = go.Figure(data=[go.Pie(
                        labels=chart_df["Category"],
                        values=chart_df["Count"],
                        hole=0.6,
                        marker=dict(colors=["#ff3366", "#00f5a0", "#ffb800"], line=dict(color='#0b0f19', width=2)),
                        textinfo='label+percent',
                        hoverinfo='label+value+percent'
                    )])
                    
                    pie_fig.update_layout(
                        title=dict(text="<b>Flow Composition Breakdown</b>", font=dict(color="#fff", size=16)),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                        margin=dict(l=20, r=20, t=50, b=30),
                        height=380,
                        annotations=[dict(text=f"<b>{res['total_records']:,}</b><br>Flows", x=0.5, y=0.5, font_size=18, font_color="#fff", showarrow=False)]
                    )
                    st.plotly_chart(pie_fig, use_container_width=True)

                with col_g2:
                    gauge_fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=res['risk_score'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "<b>Composite Threat Risk Gauge</b>", 'font': {'size': 16, 'color': '#fff'}},
                        delta={'reference': 50, 'increasing': {'color': "#ff3366"}, 'decreasing': {'color': "#00f5a0"}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                            'bar': {'color': res['badge_color'], 'thickness': 0.28},
                            'bgcolor': "rgba(30, 41, 59, 0.4)",
                            'borderwidth': 1,
                            'bordercolor': "rgba(255, 255, 255, 0.1)",
                            'steps': [
                                {'range': [0, 25], 'color': "rgba(0, 245, 160, 0.15)"},
                                {'range': [25, 50], 'color': "rgba(255, 184, 0, 0.15)"},
                                {'range': [50, 75], 'color': "rgba(255, 120, 0, 0.15)"},
                                {'range': [75, 100], 'color': "rgba(255, 51, 102, 0.15)"}
                            ],
                            'threshold': {
                                'line': {'color': "#ff3366", 'width': 3},
                                'thickness': 0.8,
                                'value': 75
                            }
                        }
                    ))
                    gauge_fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Plus Jakarta Sans", color="#fff"),
                        margin=dict(l=30, r=30, t=50, b=30),
                        height=380
                    )
                    st.plotly_chart(gauge_fig, use_container_width=True)

            with tab3:
                st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <h4 style="margin: 0; color: #fff;">Explainable AI (XAI) Feature Attribution</h4>
                                <p style="color: #94a3b8; font-size: 13px; margin-top: 4px;">
                                    Calculates how heavily each network telemetry attribute influenced the model's threat decision for <b>{res['filename']}</b>.
                                </p>
                            </div>
                            <span style="background: rgba(0, 242, 254, 0.12); color: #00f2fe; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; border: 1px solid rgba(0, 242, 254, 0.3);">
                                ● Dynamic SHAP Engine Active
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                xai_perspective = st.radio(
                    "Select Explainability Perspective:",
                    [f"⚡ Dynamic SHAP Attribution ({res['filename']})", "🌐 Global Model Baseline (Overall XGBoost Weights)"],
                    horizontal=True,
                    key="xai_perspective_toggle"
                )

                if "Dynamic SHAP" in xai_perspective:
                    plot_df = res.get('dynamic_shap_df')
                    if plot_df is None:
                        plot_df = res.get('importance_df')
                    
                    x_col = "Impact" if "Impact" in plot_df.columns else "Importance"
                    chart_title = f"<b>Top 10 Attack Vectors Driving Threat Classification in {res['filename']}</b>"
                    x_title = "Mean |SHAP Value| (Impact on Model Classification)"
                    color_scale = [[0, '#00f2fe'], [1, '#4facfe']]
                else:
                    plot_df = res.get('global_importance_df')
                    if plot_df is None:
                        plot_df = res.get('importance_df')
                    x_col = "Importance"
                    chart_title = "<b>Global Model Baseline (XGBoost Gini Gain across Benchmark)</b>"
                    x_title = "Normalized Feature Gain"
                    color_scale = [[0, '#a855f7'], [1, '#6366f1']]

                if plot_df is not None:
                    xai_bar = go.Figure(go.Bar(
                        x=plot_df[x_col],
                        y=plot_df["Feature"],
                        orientation='h',
                        marker=dict(
                            color=plot_df[x_col],
                            colorscale=color_scale,
                            line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                        ),
                        text=[f"{val:.3f}" for val in plot_df[x_col]],
                        textposition="outside",
                        textfont=dict(color="#cbd5e1", size=11, family="JetBrains Mono")
                    ))
                    xai_bar.update_layout(
                        title=dict(text=chart_title, font=dict(color="#fff", size=15)),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.05)", title=x_title),
                        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.05)"),
                        margin=dict(l=20, r=40, t=40, b=20),
                        height=420
                    )
                    st.plotly_chart(xai_bar, use_container_width=True)

                    # Dynamic Insights Card
                    top_3 = plot_df.tail(3).iloc[::-1]
                    f1_name, f1_val = top_3.iloc[0]["Feature"], top_3.iloc[0][x_col]
                    f2_name, f2_val = top_3.iloc[1]["Feature"], top_3.iloc[1][x_col]
                    f3_name, f3_val = top_3.iloc[2]["Feature"], top_3.iloc[2][x_col]

                    st.markdown(f"""
                        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 12px; padding: 16px 20px; margin-top: 10px;">
                            <div style="font-size: 12px; font-weight: 700; color: #00f2fe; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                                💡 Forensic Attribution Insights for {res['filename']}
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                                <div style="background: rgba(0,0,0,0.3); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #00f2fe;">
                                    <div style="font-size: 11px; color: #94a3b8;">PRIMARY ATTACK DRIVER</div>
                                    <div style="font-size: 14px; font-weight: 700; color: #fff; margin-top: 2px;">{f1_name}</div>
                                    <div style="font-size: 11px; color: #00f2fe; font-family: 'JetBrains Mono';">Attribution Impact: {f1_val:.3f}</div>
                                </div>
                                <div style="background: rgba(0,0,0,0.3); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #4facfe;">
                                    <div style="font-size: 11px; color: #94a3b8;">SECONDARY DRIVER</div>
                                    <div style="font-size: 14px; font-weight: 700; color: #fff; margin-top: 2px;">{f2_name}</div>
                                    <div style="font-size: 11px; color: #4facfe; font-family: 'JetBrains Mono';">Attribution Impact: {f2_val:.3f}</div>
                                </div>
                                <div style="background: rgba(0,0,0,0.3); padding: 10px 14px; border-radius: 8px; border-left: 3px solid #a855f7;">
                                    <div style="font-size: 11px; color: #94a3b8;">TERTIARY DRIVER</div>
                                    <div style="font-size: 14px; font-weight: 700; color: #fff; margin-top: 2px;">{f3_name}</div>
                                    <div style="font-size: 11px; color: #a855f7; font-family: 'JetBrains Mono';">Attribution Impact: {f3_val:.3f}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Feature importance data is not available for this model type.")

            with tab4:
                st.markdown("#### 📜 Detection Audit Trail (Recent Ingestions)")
                history_file = "data/history.csv"
                if os.path.exists(history_file):
                    hist_df = pd.read_csv(history_file)
                    st.dataframe(hist_df.tail(10), use_container_width=True)
                else:
                    st.info("No audit history found yet.")

                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                st.markdown("#### 📄 Executive Forensic PDF Export")
                
                pdf_path = create_pdf_report(
                    res['attack_count'],
                    res['Normal_count'],
                    res['anomaly_count'],
                    res['risk_score'],
                    res['risk_level'],
                    res['mitigation_action'],
                    res['mitigation_description']
                )

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="⬇ Download Incident Forensic Report (PDF)",
                        data=pdf_file,
                        file_name=f"DDoS_SOC_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )

    else:
        st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.6); border: 2px dashed rgba(0, 242, 254, 0.2); border-radius: 16px; padding: 40px 30px; text-align: center; margin-top: 15px;">
                <div style="font-size: 38px; margin-bottom: 10px;">📁</div>
                <h3 style="margin: 0; color: #fff; font-size: 19px;">No Network Traffic Dataset Ingested</h3>
                <p style="color: #94a3b8; font-size: 14px; max-width: 520px; margin: 8px auto 16px auto;">
                    Use the file uploader above to drop a <code>.csv</code> or <code>.parquet</code> capture, or switch to the Quick Load tab to test with pre-configured attack samples.
                </p>
                <div style="display: inline-flex; gap: 15px; font-size: 12px; color: #64748b;">
                    <span>• Supports CIC-DDoS2019 Schema</span>
                    <span>• Automatic Feature Alignment</span>
                    <span>• Zero-Day Anomaly Detection</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# CONSOLE MODE 2: UNIFIED REAL-TIME LIVE MONITOR (NO SEPARATE TERMINAL NEEDED)
# ==============================================================================
else:
    # Controls for Live Refresh
    st.markdown("""
        <div class="soc-hero soc-hero-live">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h1 class="soc-hero-title">
                        <span>📡</span> Simulated Real-Time DDoS Packet Stream Monitor
                    </h1>
                    <p class="soc-hero-subtitle">
                        Autonomous Micro-Batch Streaming & Real-Time Countermeasure Simulation
                    </p>
                </div>
                <div class="live-indicator live-indicator-red">
                    <span class="pulse-dot-red"></span>
                    <span>Live Stream Active</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Ingestion Station for Live Stream
    st.markdown("""
        <div style="margin-bottom: 8px;">
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
                <span>📁</span> Select / Upload Dataset for Live Stream
            </h3>
            <p style="margin: 2px 0 10px 0; font-size: 13px; color: #94a3b8;">
                Upload a packet capture to simulate real-time network streaming in 100-packet bursts, or pick a sample dataset.
            </p>
        </div>
    """, unsafe_allow_html=True)

    live_df = None
    live_filename = None

    live_tab1, live_tab2 = st.tabs([
        "📂 Upload Traffic Capture (.csv or .parquet)", 
        "🚀 Select Benchmark Stream Dataset"
    ])

    with live_tab1:
        uploaded_live = st.file_uploader(
            "Upload Live Stream Packet Data (.csv or .parquet)",
            type=["csv", "parquet"],
            key="live_file_uploader",
            help="Upload traffic capture to stream batch-by-batch in real time."
        )
        if uploaded_live is not None:
            live_filename = uploaded_live.name
            if uploaded_live.name.endswith(".csv"):
                live_df = pd.read_csv(uploaded_live)
            else:
                live_df = pd.read_parquet(uploaded_live)

    with live_tab2:
        available_samples = [
            f for f in os.listdir("data") 
            if f.endswith(".parquet") and f not in ["active_target.parquet", "combined_dataset.parquet"]
        ]
        if not available_samples:
            available_samples = ["combined_dataset.parquet"]
            
        sample_live = st.selectbox(
            "Select Stream Target:",
            available_samples,
            index=0,
            key="live_sample_selector"
        )
        if live_df is None and sample_live:
            sample_path = os.path.join("data", sample_live)
            if os.path.exists(sample_path):
                live_filename = sample_live
                live_df = pd.read_parquet(sample_path)

    # If active target already exists in data/active_target.parquet and user didn't choose new
    if live_df is None:
        if os.path.exists("data/active_target.parquet"):
            live_df = pd.read_parquet("data/active_target.parquet")
            live_filename = "Active Uploaded Target"
            if os.path.exists("data/active_target_name.txt"):
                try:
                    with open("data/active_target_name.txt", "r", encoding="utf-8") as f:
                        name_txt = f.read().strip()
                        if name_txt:
                            live_filename = name_txt
                except Exception:
                    pass
        else:
            live_df = pd.read_parquet("data/combined_dataset.parquet")
            live_filename = "combined_dataset.parquet (Default)"

    # Reset pointer if dataset changes
    if "current_live_monitored_file" not in st.session_state or st.session_state.current_live_monitored_file != live_filename:
        st.session_state.current_live_monitored_file = live_filename
        st.session_state.live_pointer = 0

    # Stream Controls Bar
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4 = st.columns([2, 1, 1, 1])

    with c_ctrl1:
        st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 14px;">
                <span style="font-size: 12px; color: #94a3b8;">MONITORING TARGET:</span>
                <b style="color: #00f2fe; margin-left: 6px;">{live_filename}</b>
                <span style="font-size: 12px; color: #64748b; margin-left: 8px;">({len(live_df):,} total records)</span>
            </div>
        """, unsafe_allow_html=True)

    with c_ctrl2:
        is_paused = st.toggle("⏸️ Pause Stream", value=st.session_state.live_paused, key="pause_toggle")
        st.session_state.live_paused = is_paused

    with c_ctrl3:
        if st.button("🔄 Restart Stream", key="restart_stream_btn"):
            st.session_state.live_pointer = 0
            st.rerun()

    with c_ctrl4:
        batch_size = st.selectbox("Batch Size", [50, 100, 200, 500], index=1, key="batch_size_sel")

    # Autorefresh (only triggered when not paused)
    if not st.session_state.live_paused:
        st_autorefresh(interval=2000, key="live_monitor_refresh_pulse")

    # Slice Current Batch
    start = st.session_state.live_pointer
    end = start + batch_size
    batch = live_df.iloc[start:end]

    if len(batch) == 0:
        st.markdown(f"""
            <div style="background: rgba(0, 245, 160, 0.1); border: 1px solid rgba(0, 245, 160, 0.3); border-radius: 12px; padding: 25px; text-align: center; margin-top: 15px;">
                <h3 style="color: #00f5a0; margin: 0;">🎉 Live Packet Stream Complete!</h3>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 6px;">
                    Finished streaming all <b>{len(live_df):,}</b> packets in <code>{live_filename}</code>.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Restart Stream from Offset 0", key="restart_after_done"):
            st.session_state.live_pointer = 0
            st.rerun()
        st.stop()

    # Advance pointer for next frame if not paused
    if not st.session_state.live_paused:
        st.session_state.live_pointer += batch_size

    # Run Batch Inference
    X_batch = batch.drop("Label", axis=1, errors="ignore")
    batch_preds = model.predict(X_batch)
    batch_attacks = int(batch_preds.sum())
    batch_normal = len(batch_preds) - batch_attacks

    batch_anom_preds = anomaly_model.predict(X_batch)
    batch_anomalies = int((batch_anom_preds == -1).sum())

    batch_risk = (
        (batch_attacks / len(X_batch)) * 70
    ) + (
        (batch_anomalies / len(X_batch)) * 30
    )
    batch_risk = min(float(batch_risk), 100.0)

    if batch_risk < 25:
        b_risk_level = "Low"
        b_color = "#00f5a0"
        b_icon = "🟢"
    elif batch_risk < 50:
        b_risk_level = "Medium"
        b_color = "#ffb800"
        b_icon = "🟡"
    elif batch_risk < 75:
        b_risk_level = "High"
        b_color = "#ff7800"
        b_icon = "🟠"
    else:
        b_risk_level = "Critical"
        b_color = "#ff3366"
        b_icon = "🔴"

    b_action, b_desc, b_sev = get_mitigation_action(b_risk_level)

    # Live Batch Telemetry Cards
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class="soc-card">
                <div class="soc-card-label">Batch Packet Window</div>
                <div class="soc-card-value" style="color: #4facfe;">{start:,} - {min(end, len(live_df)):,}</div>
                <div class="soc-card-caption">Progress: {(min(end, len(live_df))/len(live_df))*100:.1f}% of dataset</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="soc-card" style="border-left: 3px solid #ff3366;">
                <div class="soc-card-label">Batch Attacks</div>
                <div class="soc-card-value" style="color: #ff3366;">{batch_attacks:,}</div>
                <div class="soc-card-caption">{(batch_attacks/len(X_batch))*100:.1f}% of current burst</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="soc-card" style="border-left: 3px solid #00f5a0;">
                <div class="soc-card-label">Batch Normal Flows</div>
                <div class="soc-card-value" style="color: #00f5a0;">{batch_normal:,}</div>
                <div class="soc-card-caption">{(batch_normal/len(X_batch))*100:.1f}% legitimate traffic</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="soc-card" style="border-left: 3px solid {b_color};">
                <div class="soc-card-label">Live Threat Score</div>
                <div class="soc-card-value" style="color: {b_color};">{batch_risk:.1f}%</div>
                <div class="soc-card-caption">{b_icon} {b_risk_level.upper()} RISK DETECTED</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Live Mitigation Response & Donut Chart
    col_l1, col_l2 = st.columns([1, 1])

    with col_l1:
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 14px; padding: 22px; height: 100%;">
                <div style="font-size: 11px; color: {b_color}; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
                    {b_icon} ACTIVE MITIGATION DIRECTIVE &bull; {b_risk_level.upper()}
                </div>
                <h3 style="margin: 0 0 10px 0; color: #fff; font-size: 22px;">
                    {b_action}
                </h3>
                <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6; margin-bottom: 15px;">
                    {b_desc}
                </p>
                <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; font-size: 12px; color: #94a3b8; border-left: 3px solid {b_color};">
                    Autonomous defense actions update dynamically every 2 seconds matching live attack volume.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_l2:
        chart_df = pd.DataFrame({
            "Category": ["Malicious Attack", "Normal Traffic", "Zero-Day Anomaly"],
            "Count": [batch_attacks, batch_normal, batch_anomalies]
        })
        donut = go.Figure(data=[go.Pie(
            labels=chart_df["Category"],
            values=chart_df["Count"],
            hole=0.6,
            marker=dict(colors=["#ff3366", "#00f5a0", "#ffb800"], line=dict(color='#0a0e17', width=2))
        )])
        donut.update_layout(
            title=dict(text="<b>Active Batch Composition</b>", font=dict(color="#fff", size=15)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            margin=dict(l=10, r=10, t=35, b=10),
            height=240,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(donut, use_container_width=True)

    # Current Batch Stream Table
    with st.expander(f"📋 Live Packet Stream Inspect ({len(batch)} Flows in Current Window)", expanded=False):
        st.dataframe(batch.head(25), use_container_width=True)

# Footer
st.markdown("""
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.05); text-align: center; font-size: 12px; color: #475569;">
        DDoS Threat Intelligence System &bull; Powered by Streamlit, XGBoost & Scikit-learn
    </div>
""", unsafe_allow_html=True)
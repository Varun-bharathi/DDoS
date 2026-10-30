# 🛡️ Explainable Hybrid Machine Learning Framework for DDoS Defense & Real-Time Monitoring

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-brightgreen.svg)](https://xgboost.readthedocs.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainable%20AI-purple.svg)](https://shap.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, enterprise-grade **Cyber Security Operations Center (SOC) Defense Dashboard** and automated mitigation system. It combines supervised gradient boosting, unsupervised zero-day anomaly detection, per-capture **Explainable AI (SHAP)**, autonomous adaptive countermeasures, and real-time micro-batch stream monitoring into a unified high-performance application.

---

## 📌 Key Capabilities

- **Dual-Model ML Threat Engine:**
  - **Supervised XGBoost Classifier:** Detects known multi-vector DDoS attack patterns with **99.96% - 99.97% accuracy**.
  - **Unsupervised Isolation Forest:** Detects novel, zero-day network anomalies and volumetric spikes.
- **Dynamic Explainable AI (SHAP TreeExplainer):**
  - Evaluates the marginal contribution of all 77 network flow features dynamically for each uploaded dataset.
  - Switches seamlessly between **Dynamic Per-Dataset Attribution** and **Global Model Baseline**.
  - Highlights exact attack signatures (e.g., SYN/ACK flag abnormalities, packet length deviations, window size anomalies).
- **Modern Cyberpunk / SOC Dashboard:**
  - Glassmorphic dark aesthetic (`Plus Jakarta Sans` & `JetBrains Mono` typography, radial cyan/purple glows, live radar pings).
  - Dynamic top KPI cards that dynamically recalculate upon dataset ingestion.
  - Convenient file drag-and-drop ingestion directly below the metrics bar.
- **Unified In-App Real-Time Live Monitor:**
  - Both **Deep Threat Inspection** and **Real-Time Live Monitor** run inside `streamlit run app.py`—no need to launch multiple terminals.
  - Micro-batch streaming (50 to 500 packets every 2 seconds) with Pause/Resume, Restart, and live stream inspection tables.
- **Adaptive Mitigation Engine:**
  - Real-time mapping of threat severity to active countermeasures: *Monitor Traffic*, *Rate Limiting*, *Block Malicious Sources*, and *Emergency Defense*.
  - Interactive simulation toggle to demonstrate automated defense rule deployment.
- **Forensics & Audit Trail:**
  - Historical scan logging in `data/history.csv` with schema-safe migration.
  - One-click executive PDF Threat Intelligence Report generator.

---

## 🏗️ System Architecture

```text
                               ┌─────────────────────────────────┐
                               │   Network Traffic Ingestion     │
                               │ (.csv / .parquet captures)      │
                               └───────────────┬─────────────────┘
                                               │
                                               ▼
                               ┌─────────────────────────────────┐
                               │   Preprocessing & Alignment     │
                               └───────────────┬─────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       │                                               │
                       ▼                                               ▼
         ┌───────────────────────────┐                   ┌───────────────────────────┐
         │     XGBoost Classifier    │                   │      Isolation Forest     │
         │ (Supervised Classification)                   │  (Unsupervised Anomaly)   │
         └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                       │                                               │
                       ▼                                               ▼
         ┌───────────────────────────┐                   ┌───────────────────────────┐
         │   Attack / Normal Counts  │                   │    Zero-Day Anomalies     │
         └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                       │                                               │
                       └───────────────────────┬───────────────────────┘
                                               │
                                               ▼
                               ┌─────────────────────────────────┐
                               │     Risk Assessment Engine      │
                               │  Composite Weighted Threat %    │
                               └───────────────┬─────────────────┘
                                               │
                                               ▼
                               ┌─────────────────────────────────┐
                               │    Adaptive Mitigation Engine   │
                               │ (Dynamic Defense Action Mapping)│
                               └───────────────┬─────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       │                                               │
                       ▼                                               ▼
         ┌───────────────────────────┐                   ┌───────────────────────────┐
         │  🛡️ Deep Threat Console    │                   │   📡 Live Stream Radar    │
         │  • Dynamic KPI Telemetry  │                   │  • 2s Auto-Refresh Stream │
         │  • Dynamic SHAP XAI Bars  │                   │  • Pause / Resume Control │
         │  • Flow Donut & Risk Gauge│                   │  • Batch Risk Telemetry   │
         │  • Forensic Audit & PDF   │                   │  • Live Packet Table      │
         └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                       │                                               │
                       └───────────────────────┬───────────────────────┘
                                               │
                                               ▼
                               ┌─────────────────────────────────┐
                               │ Unified Web Dashboard (app.py)  │
                               │      http://localhost:8501      │
                               └─────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Backend & Logic** | **Python 3.10+** | Core data science and ML runtime |
| **Web Interface** | **Streamlit** | High-performance interactive SOC dashboard |
| **Supervised ML** | **XGBoost 2.0+** | Gradient boosted decision trees for binary traffic classification |
| **Unsupervised ML**| **Scikit-Learn** | `IsolationForest` for zero-day anomaly detection |
| **Explainable AI** | **SHAP** | `TreeExplainer` computing marginal per-flow feature attribution |
| **Stream Engine** | **streamlit-autorefresh** | Dynamic clock for automated micro-batch live streaming |
| **Data Engine** | **Pandas & PyArrow** | High-throughput columnar Parquet and CSV processing |
| **Visualization** | **Plotly Graph Objects** | Interactive dark-themed gauges, donuts, and attribution charts |
| **Reporting** | **FPDF** | Automated incident summary and forensic report PDF generation |
| **Benchmark Suite**| **CIC-DDoS2019** | Standardized realistic multi-vector DDoS attack benchmark |

---

## 📂 Project Structure

```text
DDoS/
│
├── data/
│   ├── combined_dataset.parquet   # Combined multi-vector benchmark dataset
│   ├── active_target.parquet      # Synchronized target dataset for live stream
│   ├── active_target_name.txt     # Target filename tracker
│   ├── history.csv                # Persistent audit log (risk scores & mitigation)
│   └── *-testing.parquet          # Vector samples (LDAP, DNS, Syn, MSSQL, TFTP, etc.)
│
├── models/
│   ├── xgboost_ddos_model.pkl     # Trained supervised XGBoost classifier
│   └── anomaly_detector.pkl       # Trained unsupervised Isolation Forest model
│
├── src/
│   ├── train_xgboost.py           # Supervised model training pipeline
│   ├── anomaly_detection.py       # Isolation Forest anomaly training pipeline
│   ├── combine_datasets.py        # Parquet concatenation and aggregation script
│   ├── explain.py                 # SHAP TreeExplainer baseline prototype
│   ├── inspect_data.py            # Quick dataset schema & null-value inspection
│   └── mitigation_engine.py       # Adaptive response rule mapping engine
│
├── app.py                         # Unified Cyber SOC Dashboard & Live Monitor
├── live_monitor.py                # Standalone live stream monitor (optional)
├── requirements.txt               # Project Python package dependencies
└── README.md                      # Comprehensive project documentation
```

---

## 📊 Dataset & Feature Characteristics

The system is trained and evaluated on the **CIC-DDoS2019** dataset, covering modern realistic application-layer and network-layer attacks:

### Evaluated Attack Profiles
* **Normal / Benign Traffic**
* **SYN Flood Attack**
* **DNS Amplification Attack**
* **LDAP Reflection Attack**
* **MSSQL Attack**
* **NetBIOS Attack**
* **NTP Amplification Attack**
* **SNMP Attack**
* **TFTP Attack**
* **UDP Flood Attack**
* **UDP-Lag Attack**

### Key Flow Features (77 Total Features)
* **Temporal Attributes:** Flow Duration, Flow IAT (Mean, Std, Min, Max), Forward/Backward IAT
* **Packet Statistics:** Packet Length (Min, Max, Mean, Std), Average Packet Size, Segment Size
* **Volumetric Rates:** Flow Packets/s, Flow Bytes/s, Forward Packets/s, Backward Packets/s
* **Protocol & Flags:** Protocol, FIN, SYN, RST, PSH, ACK, URG, ECE, CWR Flags
* **TCP Windowing:** Init Forward Win Bytes, Init Backward Win Bytes, Active/Idle Time

---

## 🤖 Model Performance & Evaluation

### 1. Supervised XGBoost Classifier
* **Architecture:** 100 Gradient Boosted Decision Trees, Max Depth = 6, Learning Rate = 0.1
* **Objective:** Binary cross-entropy with `logloss` evaluation metric
* **Performance:**
  * **Accuracy:** `99.96% - 99.97%`
  * **Precision:** `1.00`
  * **Recall:** `1.00`
  * **F1-Score:** `1.00`

### 2. Unsupervised Isolation Forest
* **Purpose:** Detects zero-day anomalies that deviate from typical flow distributions without requiring attack labels
* **Hyperparameters:** `contamination=0.05` (5% expected anomaly rate), `random_state=42`

---

## 📈 Dashboard Capabilities

### 1. Dynamic Executive KPI Telemetry
Four glassmorphic status cards at the top of the dashboard recalculate dynamically based on the active dataset:
* **Inspected Flows:** Total packet flows evaluated.
* **Detected Attacks:** Volume and percentage of malicious DDoS flows.
* **Normal Baseline:** Volume and percentage of legitimate network traffic.
* **Threat Risk Index:** Dynamic composite risk rating with color-coded severity badges.

### 2. Streamlined Ingestion Station
Positioned directly below the metrics bar, supporting:
* **📁 Upload Capture File:** Drag-and-drop `.csv` or `.parquet` captures up to 200MB.
* **🚀 Quick Load Benchmark:** One-click instant loader for all pre-packaged CIC-DDoS vectors (`LDAP`, `DNS`, `Syn`, `MSSQL`, etc.).

### 3. Risk Assessment Engine
Computes a composite security risk index weighted by malicious flow volume and unsupervised anomaly severity:

$$\text{Risk Score} = \left(\frac{\text{Attack Count}}{\text{Total Flows}} \times 70\right) + \left(\frac{\text{Anomaly Count}}{\text{Total Flows}} \times 30\right)$$

| Risk Score (%) | Classification | SOC Badge |
| :---: | :---: | :---: |
| `0% - 25%` | **Low Risk** | 🟢 Normal Behavior Verified |
| `25% - 50%` | **Medium Risk** | 🟡 Suspicious Bursts Detected |
| `50% - 75%` | **High Risk** | 🟠 Volumetric Assault In Progress |
| `75% - 100%` | **Critical Risk** | 🔴 Catastrophic Distributed DDoS |

### 4. Adaptive Mitigation Engine ⚡
Automatically determines and displays defense actions corresponding to the risk level:

| Risk Level | Recommended Action | Description | SOC Defense Action |
| :--- | :--- | :--- | :--- |
| **Low** | **Monitor Traffic** | Continue routine network telemetry logging. | Passive Monitoring |
| **Medium** | **Rate Limiting** | Apply flow throttling to suspicious IP source clusters. | Packet Throttling |
| **High** | **Block Suspicious Traffic** | Dynamic firewall drops matching attack flow signatures. | ACL Signature Drop |
| **Critical** | **Emergency Defense** | Upstream BGP route filtering & scrubbing center redirection. | BGP Blackholing / Scrubbing |

*Includes an interactive **"Engage Autonomous Adaptive Mitigation Rules"** checkbox to simulate real-time defense enforcement.*

### 5. Dynamic Explainable AI (SHAP TreeExplainer) 🔬
Provides interpretable insights into model decision-making:
* **⚡ Dynamic SHAP Attribution:** Computes exact marginal feature importance for the uploaded file, revealing the specific attributes driving attack classifications (e.g., `ACK Flag Count` for SYN floods vs. `Packet Length Min` for LDAP reflection).
* **🌐 Global Model Baseline:** Allows toggling to view overall XGBoost Gini Gain weights learned during training.
* **Forensic Attribution Insights:** Highlights the **Primary**, **Secondary**, and **Tertiary** attack drivers with numeric attribution scores.

### 6. Unified Real-Time Live Monitor 📡
Switch to **Real-Time Live Monitor** in the sidebar console to simulate continuous network packet streaming:
* Direct file uploader and sample selector inside the live view.
* Micro-batch streaming (50 to 500 packets every 2 seconds).
* **⏸️ Pause / Resume:** Freeze stream inspection at any time.
* **🔄 Restart:** Reset stream pointer back to packet 0.
* Dynamic batch telemetry cards, mitigation directives, and live stream inspection tables.

### 7. Audit Trail & Executive Forensic PDF Report
* Scans are automatically logged to `data/history.csv` with timestamps, counts, risk scores, and mitigation actions.
* One-click **Download Incident Forensic Report (PDF)** generates an executive PDF summary for security auditing.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Varun-bharathi/DDoS.git
cd DDoS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

*Or install required packages manually:*
```bash
pip install streamlit pandas pyarrow xgboost scikit-learn plotly joblib fpdf streamlit-autorefresh shap
```

---

## ▶️ Running the Application

### Launch the Unified Dashboard (Recommended)
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

* **To run full threat inspection:** Keep the sidebar console set to **`🛡️ Deep Threat Inspection`**. Upload or select a dataset and click **🚀 Run AI Threat Inspection**.
* **To monitor real-time packet streams:** Switch the sidebar console to **`📡 Real-Time Live Monitor`**. No separate terminal required!

*(Optional standalone launch: `streamlit run live_monitor.py` on port 8502 remains supported).*

---

## 📋 Standard Workflow

1. **Launch App:** Run `streamlit run app.py` and access the dashboard.
2. **Ingest Traffic:** Drag and drop a `.csv` or `.parquet` capture, or select a pre-packaged benchmark sample (e.g. `LDAP-testing.parquet`).
3. **Execute AI Threat Inspection:** Click **🚀 Run AI Threat Inspection** to trigger dual-model inference and SHAP attribution.
4. **Inspect Threat Intelligence Cockpit:**
   * **Tab 1:** Review incident severity, dynamic risk score, and toggle adaptive mitigation.
   * **Tab 2:** Examine flow composition donuts and the semicircular risk gauge.
   * **Tab 3:** Explore dynamic SHAP feature attributions and forensic attack driver cards.
   * **Tab 4:** Review detection audit history and export the timestamped **Forensic PDF Report**.
5. **Simulate Live Streaming:** Switch to **📡 Real-Time Live Monitor** in the sidebar to stream the capture batch-by-batch with auto-updating countermeasures.

---

## 📌 Future Enhancements

- 📡 **Real-Time Packet Sniffing:** Live interface capturing via `Scapy` / `Pyshark`.
- 🎯 **Multi-Class Attack Identification:** Granular classification distinguishing exact attack types (e.g. distinguishing SYN from NTP).
- 📧 **Automated SIEM & Alert Integration:** Webhook, Slack, and email notifications for High/Critical threat events.
- ☁️ **Containerized Cloud Deployment:** Dockerization with deployment manifests for AWS / Azure / GCP.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
# 🛡️ Explainable Hybrid Machine Learning Framework for DDoS Detection

## 📌 Project Overview
This project is an intelligent **DDoS (Distributed Denial of Service) Detection & Mitigation System** that combines supervised classification, unsupervised anomaly detection, explainable AI, adaptive defense mechanisms, and simulated live stream monitoring to protect network infrastructure.

The system integrates:
- **XGBoost Classifier** for attack detection and classification.
- **Isolation Forest** for unknown anomaly detection.
- **Explainable AI (XAI)** via feature importance analysis.
- **Interactive Streamlit Dashboard** for real-time traffic analysis and risk visualization.
- **Risk Assessment Engine** to compute composite security risk levels.
- **Adaptive Mitigation Engine** to dynamically determine defense actions based on risk levels.
- **Dynamic Live Monitoring Engine (`live_monitor.py`)** to stream and analyze datasets batch-by-batch in real time.
- **Detection History Tracking** for auditing past scans with mitigation logs.
- **PDF Report Generation** for downloadable security summaries including mitigation recommendations.

The system analyzes network traffic datasets, identifies malicious DDoS attacks with high accuracy, provides actionable insights into model decision-making, recommends automated mitigation strategies, and supports dynamic live monitoring.

---

## 🎯 Key Objectives
- **DDoS Attack Detection:** Accurately identify attack patterns in high-volume network traffic.
- **Traffic Classification:** Categorize records as **Normal** or **Attack**.
- **Anomaly Detection:** Flag novel or unseen zero-day network anomalies.
- **Risk Assessment:** Provide a unified risk score and risk level assessment.
- **Adaptive Mitigation:** Recommend and simulate real-time countermeasures (Rate Limiting, Traffic Blocking, Emergency Defense).
- **Dynamic Live Monitoring:** Stream uploaded datasets in 100-record batches every 2 seconds with live UI filename display.
- **Visual Analytics:** Offer interactive charts and data distribution previews.
- **Audit & History:** Store past detection logs and mitigation actions locally for historical reporting.
- **Report Generation:** Export concise PDF security reports containing telemetry and mitigation details.

---

## 🏗️ System Architecture
```text
                       ┌─────────────────────────┐
                       │  Network Traffic Data   │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   Data Preprocessing    │
                       └────────────┬────────────┘
                                    │
            ┌───────────────────────┴───────────────────────┐
            │                                               │
            ▼                                               ▼
┌───────────────────────┐                       ┌───────────────────────┐
│  XGBoost Classifier   │                       │   Isolation Forest    │
└───────────┬───────────┘                       └───────────┬───────────┘
            │                                               │
            ▼                                               ▼
┌───────────────────────┐                       ┌───────────────────────┐
│ Attack / Normal Count │                       │     Anomaly Count     │
└───────────┬───────────┘                       └───────────┬───────────┘
            │                                               │
            └───────────────────────┬───────────────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │  Risk Assessment Engine │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │ Adaptive Mitigation Engine
                       └────────────┬────────────┘
                                    │
            ┌───────────────────────┴───────────────────────┐
            │                                               │
            ▼                                               ▼
┌───────────────────────┐                       ┌───────────────────────┐
│ Main App (app.py)     │                       │ Live Monitor          │
│ Full Dataset Analysis │                       │ (live_monitor.py)     │
└───────────┬───────────┘                       │ 2s Batch Streaming    │
            │                                   └───────────┬───────────┘
            │                                               │
            └───────────────────────┬───────────────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   Streamlit Dashboard   │
                       └────────────┬────────────┘
                                    │
                      ┌─────────────┴─────────────┐
                      │                           │
                      ▼                           ▼
          ┌───────────────────────┐   ┌───────────────────────┐
          │ Interactive Analytics │   │  PDF Security Report  │
          └───────────────────────┘   └───────────────────────┘
```

---

## 🛠️ Technologies Used
| Technology | Purpose |
| :--- | :--- |
| **Python** | Backend logic and machine learning pipelines |
| **Streamlit** | Interactive dashboard user interface & auto-refreshed live streaming |
| **Pandas & PyArrow** | High-performance dataset processing and Parquet handling |
| **XGBoost** | Supervised DDoS attack classification |
| **Scikit-Learn** | Anomaly detection (`IsolationForest`) & model evaluation metrics |
| **Plotly** | Dynamic visual analytics and interactive charts |
| **Joblib** | Serialization and loading of trained ML models |
| **FPDF** | Automated PDF report generation |
| **CIC-DDoS2019** | Standard benchmark dataset for training and evaluation |

---

## 📂 Project Structure
```text
ddos-project/
│
├── data/
│   ├── combined_dataset.parquet   # Processed combined benchmark dataset
│   ├── active_target.parquet      # Synchronized active target dataset for live_monitor.py
│   ├── active_target_name.txt     # Stored name of currently uploaded dataset file
│   ├── history.csv                # Historical detection audit logs (includes risk level & mitigation)
│   └── *.parquet                  # Raw & subset dataset files (e.g. LDAP-training, TFTP-testing)
│
├── models/
│   ├── xgboost_ddos_model.pkl     # Trained XGBoost classifier
│   └── anomaly_detector.pkl       # Trained Isolation Forest model
│
├── src/
│   ├── train_xgboost.py           # Script to train XGBoost model
│   ├── anomaly_detection.py       # Script to train Isolation Forest model
│   ├── combine_datasets.py        # Utility to aggregate raw dataset files
│   ├── explain.py                 # Feature importance and explainability logic
│   ├── inspect_data.py            # Dataset inspection tool
│   ├── risk_engine.py             # Risk calculation helper
│   └── mitigation_engine.py       # Adaptive mitigation rule engine
│
├── app.py                         # Main Streamlit web dashboard application
├── live_monitor.py                # Simulated live network traffic monitor (synchronized with app.py)
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```

---

## 📊 Dataset Information
This framework uses the **CIC-DDoS2019 Dataset**, a standard benchmark for DDoS attack detection containing modern network attack profiles.

### Covered Attack Types:
- **Normal Traffic**
- **DNS Attack**
- **LDAP Attack**
- **MSSQL Attack**
- **NetBIOS Attack**
- **NTP Attack**
- **SNMP Attack**
- **SYN Flood Attack**
- **TFTP Attack**
- **UDP Attack**
- **UDP-Lag Attack**

### Key Features (77 Total Features):
- **Flow Duration & Timestamps**
- **Packet Length Statistics** (Min, Max, Mean, Std)
- **Flow Rates:** Flow Bytes/s, Flow Packets/s
- **Directional Counts:** Fwd Packets, Bwd Packets
- **Packet Header & Flag Statistics**
- **Network Protocol Information**

---

## 🤖 Machine Learning Models

### 1. XGBoost Classifier (Supervised Classification)
- **Purpose:** Classifies incoming traffic into **Normal (0)** or **DDoS Attack (1)**.
- **Model Configuration:**
  - `n_estimators`: 100
  - `max_depth`: 6
  - `learning_rate`: 0.1
  - `eval_metric`: `logloss`
- **Performance Metrics:**
  - **Accuracy:** `99.96%`
  - **Precision:** `1.00`
  - **Recall:** `1.00`
  - **F1-Score:** `1.00`

### 2. Isolation Forest (Unsupervised Anomaly Detection)
- **Purpose:** Flags zero-day anomalies and outliers in network traffic patterns.
- **Model Configuration:**
  - `contamination`: `0.05` (5% expected anomaly rate)
  - `random_state`: `42`

---

## 📈 Dashboard & Features

### 1. Dataset Preview & Telemetry
- Previews the first 5 records of uploaded CSV or Parquet files.
- Displays total row count and feature column count.

### 2. Detection Results
- Real-time count of **Attack Records**, **Normal Records**, and detected **Anomalies**.

### 3. Risk Assessment Engine
Calculates a composite risk score weighted by attack volume and anomaly severity:
$$\text{Risk Score} = \left(\frac{\text{Attack Count}}{\text{Total Records}} \times 70\right) + \left(\frac{\text{Anomaly Count}}{\text{Total Records}} \times 30\right)$$

#### Risk Level Breakdown:
| Risk Score Range (%) | Risk Level | Dashboard Indicator |
| :---: | :---: | :---: |
| `0 - 25%` | **Low** | 🟢 Low Risk |
| `25 - 50%` | **Medium** | 🟡 Medium Risk |
| `50 - 75%` | **High** | 🟠 High Risk |
| `75 - 100%` | **Critical** | 🔴 Critical Risk |

### 4. Adaptive Mitigation Engine ⚡
Determines and displays automated mitigation responses corresponding to the evaluated risk level:

| Risk Level | Recommended Action | Description | Severity | Dashboard Banner |
| :--- | :--- | :--- | :--- | :--- |
| **Low** | **Monitor Traffic** | Continue monitoring network activity. | `Low` | `st.success()` |
| **Medium** | **Rate Limiting** | Apply traffic throttling to suspicious traffic. | `Medium` | `st.warning()` |
| **High** | **Block Suspicious Traffic** | Simulate blocking malicious traffic sources. | `High` | `st.error()` |
| **Critical** | **Emergency Defense** | Simulate blocking traffic and triggering security alerts. | `Critical` | `st.error()` |

- **Interactive Defense Toggle:** Includes an **"Enable Adaptive Mitigation"** checkbox that simulates real-time defense enforcement and provides active alert status notifications.

### 5. Dynamic Live Stream Monitoring (`live_monitor.py`) 📡
- **Dataset Synchronization:** Automatically streams whichever dataset file you select in `app.py` (e.g. `LDAP-training.parquet`, `TFTP-testing.parquet`).
- **UI Filename Header:** Prominently displays the exact name of the file being monitored:
  `📁 Currently Monitoring File: LDAP-training.parquet (Uploaded File) | 📊 Total Records: 6,715`
- **Auto-Refresh Streaming:** Streams 100-record batches every 2 seconds.
- **Batch Adaptive Mitigation:** Evaluates and updates mitigation alert banners dynamically for each streaming batch.

### 6. Interactive Visualizations
- **Traffic Distribution:** Pie chart breaking down Attack, Normal, and Anomaly traffic.
- **Risk Score Analysis:** Bar chart displaying the calculated threat score.
- **Feature Importance Chart:** Horizontal bar chart highlighting top features driving model predictions.

### 7. Detection History Tracking
- Automatically records scan logs into `data/history.csv`.
- Logs timestamp, attack counts, normal counts, anomaly counts, risk score, **risk level**, and **mitigation action**.
- Displays recent scan history table in the dashboard.

### 8. PDF Report Generation
- Exports a downloadable `.pdf` summary report containing scan telemetry, risk score, risk level, **mitigation action**, **mitigation description**, and generation timestamp.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ddos-project
```

### 2. Install Dependencies
Install all required libraries using `requirements.txt`:
```bash
pip install -r requirements.txt
```
*Or manually install individual dependencies:*
```bash
pip install streamlit pandas pyarrow xgboost scikit-learn plotly joblib fpdf streamlit-autorefresh
```

---

## ▶️ Running the Application

### Step 1: Train Models (Optional)
If you wish to retrain the machine learning models on updated data:
```bash
python src/train_xgboost.py
python src/anomaly_detection.py
```

### Step 2: Launch Main Dashboard
Run the main Streamlit application:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

### Step 3: Launch Live Monitor (Optional)
Run the simulated live monitoring dashboard in a separate terminal:
```bash
streamlit run live_monitor.py
```
Open your browser and navigate to `http://localhost:8502`.

---

## 📋 Application Workflow
1. **Upload Dataset:** Select a network traffic dataset (e.g. `LDAP-training.parquet`) in `app.py`.
2. **Preview Data:** Verify dataset columns and record counts.
3. **Run Detection:** Click **🚀 Detect Attack** to execute predictions on the complete dataset.
4. **Review Adaptive Mitigation:** Inspect recommended mitigation actions and toggle **Enable Adaptive Mitigation** to simulate real-time enforcement.
5. **Stream Live Traffic:** Open `live_monitor.py` (`streamlit run live_monitor.py`) to watch the uploaded file (`LDAP-training.parquet`) stream live in 100-record batches every 2 seconds with dynamic UI filename tracking.
6. **Analyze Charts:** Inspect pie charts, risk bar charts, and feature importance graphs.
7. **Audit Detection History:** Review historical scan records with logged risk levels and mitigation actions.
8. **Download Report:** Click **⬇ Download PDF Report** to save a timestamped summary including mitigation details.

---

## 📌 Future Enhancements
- 📡 **Real-Time Packet Sniffing:** Live network capture using `Scapy` / `Pyshark`.
- 🔍 **SHAP Integration:** Deep explainability visualizations for individual traffic flows.
- 🎯 **Multi-Class Classification:** Granular identification of specific attack types (SYN, UDP, NTP).
- 📧 **Automated Alerting:** Email / Slack notifications upon detecting Critical risk levels.
- ☁️ **Cloud Deployment:** Containerization with Docker and deployment on AWS / GCP.
- 🛡️ **SOC Dashboard Integration:** Integration with SIEM platforms (Splunk, Elastic Stack).
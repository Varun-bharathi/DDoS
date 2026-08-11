# 🛡️ Explainable Hybrid Machine Learning Framework for DDoS Detection

## 📌 Project Overview

This project is an intelligent **DDoS (Distributed Denial of Service) Detection System** that combines supervised classification, unsupervised anomaly detection, and explainable AI to protect network infrastructure.

The system integrates:
- **XGBoost Classifier** for attack detection and classification.
- **Isolation Forest** for unknown anomaly detection.
- **Explainable AI (XAI)** via feature importance analysis.
- **Simulated Live Monitoring Engine** for real-time streaming traffic analysis.
- **Interactive Streamlit Dashboard** for real-time traffic analysis and risk visualization.
- **Risk Assessment Engine** to compute composite security risk levels.
- **Detection History Tracking** for auditing past scans.
- **PDF Report Generation** for downloadable security summaries.

The system analyzes network traffic datasets, identifies malicious DDoS attacks with high accuracy, and provides actionable insights into model decision-making.

---

## 🎯 Key Objectives

- **DDoS Attack Detection:** Accurately identify attack patterns in high-volume network traffic.
- **Traffic Classification:** Categorize records as **Benign** or **Attack**.
- **Anomaly Detection:** Flag novel or unseen zero-day network anomalies.
- **Simulated Live Streaming:** Stream network flows to showcase real-time threat detection.
- **Risk Assessment:** Provide a unified risk score and risk level assessment.
- **Visual Analytics:** Offer interactive charts and data distribution previews.
- **Audit & History:** Store past detection logs locally for historical reporting.
- **Report Generation:** Export concise PDF security reports for analysis and documentation.

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
│ Attack / Benign Count │                       │     Anomaly Count     │
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
| **Streamlit** | Interactive dashboard user interface |
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
│   ├── combined_dataset.parquet   # Processed combined dataset
│   ├── history.csv                # Historical detection audit logs
│   └── *.parquet                  # Raw & subset dataset files
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
│   └── risk_engine.py             # Risk calculation helper
│
├── app.py                         # Main Streamlit web dashboard application
├── live_monitor.py                # Standalone live streaming monitoring script
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation
```

---

## 📊 Dataset Information

This framework uses the **CIC-DDoS2019 Dataset**, a standard benchmark for DDoS attack detection containing modern network attack profiles.

### Covered Attack Types:
- **Benign Traffic**
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
- **Purpose:** Classifies incoming traffic into **Benign (0)** or **DDoS Attack (1)**.
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
- Real-time count of **Attack Records**, **Benign Records**, and detected **Anomalies**.

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

### 4. Interactive Visualizations
- **Traffic Distribution:** Pie chart breaking down Attack, Benign, and Anomaly traffic.
- **Risk Score Analysis:** Bar chart displaying the calculated threat score.
- **Feature Importance Chart:** Horizontal bar chart highlighting top features driving model predictions.

### 5. Detection History Tracking
- Automatically records scan logs into `data/history.csv`.
- Displays recent scan history table with timestamps and metrics.

### 6. PDF Report Generation
- Exports a downloadable `.pdf` summary report containing scan telemetry, risk score, risk level, and timestamp.

---

## 🔴 Simulated Live Monitoring

### Overview
The project includes a **Simulated Live Monitoring Module** that mimics real-time network traffic analysis using historical data from the **CIC-DDoS2019** dataset.

Instead of intercepting live network packets via hardware interfaces, the system continuously reads records row-by-row from the dataset and feeds them into the trained machine learning pipeline. This simulates live network traffic streaming and dynamic dashboard updates.

---

### Why Simulated Monitoring?

Full real-time packet capture typically requires:
- Deep packet inspection tools (**Wireshark**, **Scapy**, **PyShark**).
- **Administrator / Root Privileges** for raw socket access.
- Live active network traffic on dedicated network interface cards (NICs).

For project demonstrations, research presentations, and academic viva evaluations, **Simulated Live Monitoring** provides the exact same operational workflow and dashboard metrics without requiring complex network configurations or elevated permissions.

---

### Working Principle & Flow

```text
               ┌─────────────────────────┐
               │    Historical Dataset   │
               └────────────┬────────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │    Read Next Record     │
               └────────────┬────────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │   XGBoost Prediction    │
               │   (Attack vs Benign)    │
               └────────────┬────────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │ Isolation Forest Check  │
               │  (Anomaly Detection)    │
               └────────────┬────────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │ Dynamic Risk Assessment │
               └────────────┬────────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │ Dashboard Metrics Sync  │
               └────────────┬────────────┘
                            │
                            └────► Repeat for Next Record
```

---

### Model Components & Prediction Logic

1. **XGBoost Classifier:**
   - Evaluates flow features and outputs class label:
     - `0` $\rightarrow$ **Benign Traffic**
     - `1` $\rightarrow$ **DDoS Attack**

2. **Isolation Forest:**
   - Detects statistical distribution anomalies:
     - `1` $\rightarrow$ **Normal Flow**
     - `-1` $\rightarrow$ **Anomaly Detected**

3. **Streamlit Dashboard Telemetry:**
   - Updates live packet count, attack percentage, benign count, anomaly count, composite risk score, and real-time activity logs.

---

### Live Risk Calculation

As streaming records are processed, the **Risk Assessment Engine** continuously updates the risk score:

$$\text{Risk Score} = \left(\text{Attack Percentage} \times 0.70\right) + \left(\text{Anomaly Percentage} \times 0.30\right)$$

#### Example Calculation:
If a stream of records results in **80% Attack Records** and **20% Anomalies**:
$$\text{Risk Score} = (80 \times 0.70) + (20 \times 0.30) = 56 + 6 = 62\% \quad \Rightarrow \quad \text{🟠 High Risk}$$

#### Real-Time Status Alerts:
- ⚠️ **DDoS Attack Detected:** Triggered when attack volume spikes.
- ✅ **Traffic Normal:** Displayed when benign traffic dominates.

---

### Key Advantages

- ✔ **Real-Time Simulation:** Demonstrates streaming traffic ingestion and dynamic threat detection.
- ✔ **Zero Dependency on Raw Sockets:** No Wireshark or Scapy network sniffing required.
- ✔ **No Admin Rights Required:** Runs seamlessly in standard user environments.
- ✔ **Easy Demonstration:** Ideal for viva, academic presentations, and quick prototyping.

---

### Future Upgrade Path to Native Real-Time Capture

The simulated streaming architecture is designed to be fully modular, allowing seamless upgrades to live packet capture using:
- **PyShark (`pyshark`)** or **Scapy (`scapy.all.sniff`)** attached to Wi-Fi or Ethernet interfaces.
- **Real-Time Packet Dissector:** Extracts 77 flow features live from captured PCAP frames.

```text
Live Packets ──► Feature Extractor ──► XGBoost + Isolation Forest ──► Risk Engine ──► Alert & Block
```

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
pip install streamlit pandas pyarrow xgboost scikit-learn plotly joblib fpdf
```

---

## ▶️ Running the Application

### Step 1: Train Models (Optional)
If you wish to retrain the machine learning models on updated data:
```bash
python src/train_xgboost.py
python src/anomaly_detection.py
```

### Step 2: Launch Dashboard
Run the Streamlit web dashboard:
```bash
streamlit run app.py
```

### Step 3: Run Live Monitoring Module (Optional)
To execute the streaming live monitoring module:
```bash
python live_monitor.py
```

Open your browser and navigate to:
```text
http://localhost:8501
```

---

## 📋 Application Workflow

1. **Upload Dataset:** Select a network traffic dataset (`.csv` or `.parquet`).
2. **Preview Data:** Verify dataset columns and record counts.
3. **Run Detection:** Click **🚀 Detect Attack** to execute predictions.
4. **View Metrics:** Review classified traffic counts, anomaly flags, and the composite risk score.
5. **Simulate Live Stream:** Monitor real-time streaming traffic telemetry.
6. **Analyze Charts:** Inspect pie charts, risk bar charts, and feature importance graphs.
7. **Download Report:** Click **⬇ Download PDF Report** to save a timestamped summary.

---

## 📌 Future Enhancements

- 📡 **Real-Time Packet Sniffing:** Live network capture using `Scapy` / `Pyshark`.
- 🔍 **SHAP Integration:** Deep explainability visualizations for individual traffic flows.
- 🎯 **Multi-Class Classification:** Granular identification of specific attack types (SYN, UDP, NTP).
- 📧 **Automated Alerting:** Email / Slack notifications upon detecting Critical risk levels.
- ☁️ **Cloud Deployment:** Containerization with Docker and deployment on AWS / GCP.
- 🛡️ **SOC Dashboard Integration:** Integration with SIEM platforms (Splunk, Elastic Stack).

# 🛡️ Explainable Hybrid Machine Learning Framework for DDoS Detection

## 📌 Project Overview

This project is an intelligent **DDoS (Distributed Denial of Service) Detection System** that combines supervised classification, unsupervised anomaly detection, and explainable AI to protect network infrastructure.

The system integrates:
- **XGBoost Classifier** for attack detection and classification.
- **Isolation Forest** for unknown anomaly detection.
- **Explainable AI (XAI)** via feature importance analysis.
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
5. **Analyze Charts:** Inspect pie charts, risk bar charts, and feature importance graphs.
6. **Download Report:** Click **⬇ Download PDF Report** to save a timestamped summary.

---

## 📌 Future Enhancements

- 📡 **Real-Time Packet Sniffing:** Live network capture using `Scapy` / `Pyshark`.
- 🔍 **SHAP Integration:** Deep explainability visualizations for individual traffic flows.
- 🎯 **Multi-Class Classification:** Granular identification of specific attack types (SYN, UDP, NTP).
- 📧 **Automated Alerting:** Email / Slack notifications upon detecting Critical risk levels.
- ☁️ **Cloud Deployment:** Containerization with Docker and deployment on AWS / GCP.
- 🛡️ **SOC Dashboard Integration:** Integration with SIEM platforms (Splunk, Elastic Stack).

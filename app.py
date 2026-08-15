# # import streamlit as st
# # import pandas as pd
# # import joblib

# # # Page Config
# # st.set_page_config(
# #     page_title="DDoS Detection Dashboard",
# #     page_icon="🛡️",
# #     layout="wide"
# # )

# # # Load Models
# # model = joblib.load("models/xgboost_ddos_model.pkl")
# # anomaly_model = joblib.load("models/anomaly_detector.pkl")

# # # Title
# # st.title("🛡️ DDoS Detection Dashboard")

# # # Metrics
# # col1, col2, col3, col4 = st.columns(4)

# # with col1:
# #     st.metric("Total Traffic", "306K")

# # with col2:
# #     st.metric("Detected Attacks", "255K")

# # with col3:
# #     st.metric("Normal Traffic", "51K")

# # with col4:
# #     st.metric("Model Accuracy", "99.97%")

# # # Upload Section
# # st.subheader("Upload Traffic File")

# # uploaded_file = st.file_uploader(
# #     "Choose a CSV or Parquet file",
# #     type=["csv", "parquet"]
# # )

# # if uploaded_file:

# #     st.success("File Uploaded Successfully")

# #     # Read File
# #     if uploaded_file.name.endswith(".csv"):
# #         df = pd.read_csv(uploaded_file)
# #     else:
# #         df = pd.read_parquet(uploaded_file)

# #     # Preview
# #     st.subheader("Dataset Preview")
# #     st.dataframe(df.head())

# #     # Detect Button
# #     if st.button("Detect Attack"):

# #         try:
# #             # Remove label if present
# #             X = df.drop("Label", axis=1, errors="ignore")

# #             # XGBoost Prediction
# #             predictions = model.predict(X)

# #             attack_count = int(sum(predictions))
# #             Normal_count = len(predictions) - attack_count

# #             # Isolation Forest Prediction
# #             anomaly_predictions = anomaly_model.predict(X)

# #             anomaly_count = int(
# #                 (anomaly_predictions == -1).sum()
# #             )

# #             # Results
# #             st.subheader("Detection Results")

# #             col1, col2, col3 = st.columns(3)

# #             with col1:
# #                 st.metric(
# #                     "Attack Records",
# #                     attack_count
# #                 )

# #             with col2:
# #                 st.metric(
# #                     "Normal Records",
# #                     Normal_count
# #                 )

# #             with col3:
# #                 st.metric(
# #                     "Anomalies",
# #                     anomaly_count
# #                 )

# #             # Detection Status
# #             if attack_count > Normal_count:
# #                 st.error("⚠️ DDoS Attack Detected")
# #             else:
# #                 st.success("✅ Mostly Normal Traffic")

# #             # Risk Score
# #             risk_score = (
# #                 (attack_count / len(X)) * 70
# #             ) + (
# #                 (anomaly_count / len(X)) * 30
# #             )

# #             st.subheader("Risk Assessment")

# #             st.progress(min(int(risk_score), 100))

# #             st.write(
# #                 f"Risk Score: {risk_score:.2f}%"
# #             )

# #             # Risk Level
# #             if risk_score < 25:
# #                 st.success("🟢 Low Risk")

# #             elif risk_score < 50:
# #                 st.warning("🟡 Medium Risk")

# #             elif risk_score < 75:
# #                 st.warning("🟠 High Risk")

# #             else:
# #                 st.error("🔴 Critical Risk")

# #         except Exception as e:
# #             st.error(f"Error: {e}")

# import streamlit as st
# import pandas as pd
# import joblib
# import plotly.express as px

# # =========================
# # Page Configuration
# # =========================

# st.set_page_config(
#     page_title="DDoS Detection Dashboard",
#     page_icon="🛡️",
#     layout="wide"
# )

# # =========================
# # Load Models
# # =========================

# model = joblib.load("models/xgboost_ddos_model.pkl")
# anomaly_model = joblib.load("models/anomaly_detector.pkl")

# # =========================
# # Title
# # =========================

# st.title("🛡️ Explainable Hybrid ML Framework for DDoS Detection")

# # =========================
# # Top Metrics
# # =========================

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric("Total Traffic", "306K")

# with col2:
#     st.metric("Detected Attacks", "255K")

# with col3:
#     st.metric("Normal Traffic", "51K")

# with col4:
#     st.metric("Model Accuracy", "99.97%")

# # =========================
# # File Upload
# # =========================

# st.subheader("📂 Upload Traffic Dataset")

# uploaded_file = st.file_uploader(
#     "Choose CSV or Parquet File",
#     type=["csv", "parquet"]
# )

# if uploaded_file:

#     st.success("✅ File Uploaded Successfully")

#     # =========================
#     # Read File
#     # =========================

#     if uploaded_file.name.endswith(".csv"):
#         df = pd.read_csv(uploaded_file)
#     else:
#         df = pd.read_parquet(uploaded_file)

#     # =========================
#     # Dataset Preview
#     # =========================

#     st.subheader("📋 Dataset Preview")
#     st.dataframe(df.head())

#     st.write(f"Rows: {df.shape[0]}")
#     st.write(f"Columns: {df.shape[1]}")

#     # =========================
#     # Detection Button
#     # =========================

#     if st.button("🚀 Detect Attack"):

#         try:

#             # Remove Label if present
#             X = df.drop("Label", axis=1, errors="ignore")

#             # =========================
#             # XGBoost Prediction
#             # =========================

#             predictions = model.predict(X)

#             attack_count = int(sum(predictions))
#             Normal_count = len(predictions) - attack_count

#             # =========================
#             # Isolation Forest
#             # =========================

#             anomaly_predictions = anomaly_model.predict(X)

#             anomaly_count = int(
#                 (anomaly_predictions == -1).sum()
#             )

#             # =========================
#             # Detection Results
#             # =========================

#             st.subheader("🔍 Detection Results")

#             c1, c2, c3 = st.columns(3)

#             with c1:
#                 st.metric(
#                     "Attack Records",
#                     attack_count
#                 )

#             with c2:
#                 st.metric(
#                     "Normal Records",
#                     Normal_count
#                 )

#             with c3:
#                 st.metric(
#                     "Anomalies",
#                     anomaly_count
#                 )

#             # =========================
#             # Detection Status
#             # =========================

#             if attack_count > Normal_count:
#                 st.error("⚠️ DDoS Attack Detected")
#             else:
#                 st.success("✅ Mostly Normal Traffic")

#             # =========================
#             # Risk Score
#             # =========================

#             risk_score = (
#                 (attack_count / len(X)) * 70
#             ) + (
#                 (anomaly_count / len(X)) * 30
#             )

#             st.subheader("🛡️ Risk Assessment")

#             st.progress(min(int(risk_score), 100))

#             st.write(
#                 f"Risk Score: {risk_score:.2f}%"
#             )

#             # =========================
#             # Risk Level
#             # =========================

#             if risk_score < 25:
#                 st.success("🟢 Low Risk")

#             elif risk_score < 50:
#                 st.warning("🟡 Medium Risk")

#             elif risk_score < 75:
#                 st.warning("🟠 High Risk")

#             else:
#                 st.error("🔴 Critical Risk")

#             # =========================
#             # Traffic Distribution Chart
#             # =========================

#             st.subheader("📊 Traffic Distribution")

#             chart_df = pd.DataFrame({
#                 "Category": [
#                     "Attack",
#                     "Normal",
#                     "Anomaly"
#                 ],
#                 "Count": [
#                     attack_count,
#                     Normal_count,
#                     anomaly_count
#                 ]
#             })

#             pie_fig = px.pie(
#                 chart_df,
#                 names="Category",
#                 values="Count",
#                 title="Traffic Analysis"
#             )

#             st.plotly_chart(
#                 pie_fig,
#                 width="stretch"
#             )

#             # =========================
#             # Risk Score Chart
#             # =========================

#             st.subheader("📈 Risk Score Analysis")

#             risk_df = pd.DataFrame({
#                 "Metric": ["Risk Score"],
#                 "Value": [risk_score]
#             })

#             bar_fig = px.bar(
#                 risk_df,
#                 x="Metric",
#                 y="Value",
#                 title="Current Risk Level"
#             )

#             st.plotly_chart(
#                 bar_fig,
#                 width="stretch"
#             )

#         except Exception as e:
#             st.error(f"Error: {e}")


import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os
import datetime
from fpdf import FPDF
import tempfile
from src.mitigation_engine import get_mitigation_action  # Integration: Import adaptive mitigation module

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="DDoS Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# =====================================
# Load Models
# =====================================

model = joblib.load("models/xgboost_ddos_model.pkl")
anomaly_model = joblib.load("models/anomaly_detector.pkl")


from fpdf import FPDF
import tempfile
import datetime

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

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        200,
        10,
        "DDoS Detection Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        200,
        10,
        f"Attack Records: {attack_count}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Normal Records: {Normal_count}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Anomaly Records: {anomaly_count}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Risk Score: {risk_score:.2f}%",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Risk Level: {risk_level}",
        ln=True
    )

    # Integration Point: Append adaptive mitigation details to the PDF summary report
    pdf.cell(
        200,
        10,
        f"Mitigation Action: {mitigation_action}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Mitigation Description: {mitigation_description}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Generated On: {datetime.datetime.now()}",
        ln=True
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    pdf.output(temp_file.name)

    return temp_file.name

# =====================================
# Header
# =====================================

st.title("🛡️ Explainable Hybrid ML Framework for DDoS Detection")

# =====================================
# Dashboard Metrics
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Traffic", "306K")

with col2:
    st.metric("Detected Attacks", "255K")

with col3:
    st.metric("Normal Traffic", "51K")

with col4:
    st.metric("Model Accuracy", "99.97%")

# =====================================
# File Upload
# =====================================

st.subheader("📂 Upload Traffic Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV or Parquet File",
    type=["csv", "parquet"]
)

if uploaded_file is not None:

    st.success("✅ File Uploaded Successfully")

    # =====================================
    # Read Dataset
    # =====================================

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_parquet(uploaded_file)

    # =====================================
    # Preview
    # =====================================

    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())

    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    # =====================================
    # Detect Button
    # =====================================

    if st.button("🚀 Detect Attack"):

        try:

            X = df.drop(
                "Label",
                axis=1,
                errors="ignore"
            )

            # XGBoost Prediction
            predictions = model.predict(X)

            attack_count = int(predictions.sum())
            Normal_count = len(predictions) - attack_count

            # Isolation Forest
            anomaly_predictions = anomaly_model.predict(X)

            anomaly_count = int(
                (anomaly_predictions == -1).sum()
            )

            # =====================================
            # Detection Results
            # =====================================

            st.subheader("🔍 Detection Results")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Attack Records",
                    attack_count
                )

            with c2:
                st.metric(
                    "Normal Records",
                    Normal_count
                )

            with c3:
                st.metric(
                    "Anomalies",
                    anomaly_count
                )

            # =====================================
            # Detection Status
            # =====================================

            if attack_count > Normal_count:
                st.error("⚠️ DDoS Attack Detected")
            else:
                st.success("✅ Mostly Normal Traffic")

            # =====================================
            # Risk Score
            # =====================================

            risk_score = (
                (attack_count / len(X)) * 70
            ) + (
                (anomaly_count / len(X)) * 30
            )

            st.subheader("🛡️ Risk Assessment")

            st.progress(
                min(int(risk_score), 100)
            )

            st.write(
                f"Risk Score: {risk_score:.2f}%"
            )

            if risk_score < 25:
                risk_level = "Low"
                st.success("🟢 Low Risk")

            elif risk_score < 50:
                risk_level = "Medium"
                st.warning("🟡 Medium Risk")

            elif risk_score < 75:
                risk_level = "High"
                st.warning("🟠 High Risk")

            else:
                risk_level = "Critical"
                st.error("🔴 Critical Risk")

            # =====================================
            # Adaptive Mitigation Section
            # =====================================
            # Integration Point: Retrieve mitigation parameters based on calculated risk_level
            mitigation_action, mitigation_description, severity = get_mitigation_action(risk_level)

            st.subheader("⚡ Adaptive Mitigation")

            # Display Risk Level, Recommended Action, and Description in color-coded alert box
            alert_text = (
                f"**Risk Level:** {risk_level}\n\n"
                f"**Recommended Action:** {mitigation_action}\n\n"
                f"**Description:** {mitigation_description}"
            )

            if risk_level == "Low":
                st.success(alert_text)
            elif risk_level == "Medium":
                st.warning(alert_text)
            elif risk_level == "High":
                st.error(alert_text)
            else:  # Critical
                st.error(alert_text)

            # Integration Point: Streamlit checkbox to activate mitigation simulation
            enable_mitigation = st.checkbox("Enable Adaptive Mitigation")

            if enable_mitigation:
                if risk_level == "Low":
                    st.info("ℹ️ Monitoring traffic activity in real-time...")
                elif risk_level == "Medium":
                    st.warning("⚡ Rate limiting activated on suspicious traffic.")
                elif risk_level == "High":
                    st.error("🚫 Blocking suspicious traffic activated.")
                else:  # Critical
                    st.error("🚨 Emergency defense activated! Blocking traffic and triggering security alerts.")

            # =====================================
            # Traffic Distribution Pie Chart
            # =====================================

            st.subheader("📊 Traffic Distribution")

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

            pie_fig = px.pie(
                chart_df,
                names="Category",
                values="Count",
                title="Traffic Analysis"
            )

            st.plotly_chart(
                pie_fig,
                width="stretch"
            )

            # =====================================
            # Risk Score Chart
            # =====================================

            st.subheader("📈 Risk Score Analysis")

            risk_df = pd.DataFrame({
                "Metric": ["Risk Score"],
                "Value": [risk_score]
            })

            bar_fig = px.bar(
                risk_df,
                x="Metric",
                y="Value",
                title="Current Risk Level"
            )

            st.plotly_chart(
                bar_fig,
                width="stretch"
            )

            # =====================================
            # Feature Importance
            # =====================================

            st.subheader(
                "🔬 Top 10 Important Features"
            )

            importance_df = pd.DataFrame({
                "Feature": X.columns,
                "Importance": model.feature_importances_
            })

            importance_df = (
                importance_df
                .sort_values(
                    "Importance",
                    ascending=False
                )
                .head(10)
            )

            st.dataframe(
                importance_df,
                width="stretch"
            )

            # =====================================
            # Feature Importance Chart
            # =====================================

            st.subheader(
                "📊 Feature Importance Chart"
            )

            feature_fig = px.bar(
                importance_df,
                x="Importance",
                y="Feature",
                orientation="h",
                title="Top Features Used By XGBoost"
            )

            st.plotly_chart(
                feature_fig,
                width="stretch"
            )

            # =====================================
            # Detection History
            # =====================================
            # Integration Point: Extend detection history dataframe to log risk_level and mitigation_action
            history = pd.DataFrame({
                "Timestamp": [
                    datetime.datetime.now()
                ],
                "Attack Count": [
                    attack_count
                ],
                "Normal Count": [
                    Normal_count
                ],
                "Anomaly Count": [
                    anomaly_count
                ],
                "Risk Score": [
                    round(risk_score, 2)
                ],
                "risk_level": [
                    risk_level
                ],
                "mitigation_action": [
                    mitigation_action
                ]
            })

            history_file = "data/history.csv"
            if os.path.exists(history_file):
                existing_df = pd.read_csv(history_file)
                # Schema Migration: Ensure existing CSV file includes risk_level and mitigation_action columns
                if "risk_level" not in existing_df.columns:
                    existing_df["risk_level"] = "N/A"
                if "mitigation_action" not in existing_df.columns:
                    existing_df["mitigation_action"] = "N/A"
                existing_df.to_csv(history_file, index=False)

                history.to_csv(
                    history_file,
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                history.to_csv(
                    history_file,
                    index=False
                )

            st.subheader("📜 Detection History")

            history_df = pd.read_csv(
                history_file
            )

            st.dataframe(
                history_df.tail(10),
                width="stretch"
            )

            st.subheader("📄 Download Report")

            # Integration Point: Pass mitigation action and description to PDF report generator
            pdf_path = create_pdf_report(
                attack_count,
                Normal_count,
                anomaly_count,
                risk_score,
                risk_level,
                mitigation_action,
                mitigation_description
            )

            with open(pdf_path, "rb") as pdf_file:

                st.download_button(
                    label="⬇ Download PDF Report",
                    data=pdf_file,
                    file_name="DDoS_Report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"Error: {e}")
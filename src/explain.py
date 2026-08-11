import pandas as pd
import joblib
import shap

# Load model
model = joblib.load("models/xgboost_ddos_model.pkl")

# Load dataset
df = pd.read_parquet("data/combined_dataset.parquet")

X = df.drop("Label", axis=1)

# Create explainer
explainer = shap.TreeExplainer(model)

# Generate SHAP values for first 100 rows
shap_values = explainer.shap_values(X.iloc[:100])

print("SHAP Integration Successful!")
print("Shape:", len(shap_values))
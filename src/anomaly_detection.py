import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# Load data
df = pd.read_parquet("data/combined_dataset.parquet")

# Remove label column
X = df.drop("Label", axis=1)

# Train anomaly detector
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Save model
joblib.dump(
    model,
    "models/anomaly_detector.pkl"
)

print("Anomaly Detector Saved!")
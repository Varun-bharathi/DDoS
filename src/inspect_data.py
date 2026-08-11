import pandas as pd
import os

# Change this to one of your parquet files
file_path = "data/Syn-training.parquet"

df = pd.read_parquet(file_path)

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nInfo:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))
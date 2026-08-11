import pandas as pd

df = pd.read_parquet("data/UDP-testing.parquet")

print(df["Label"].value_counts())
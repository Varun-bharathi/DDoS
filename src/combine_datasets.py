import pandas as pd

files = [
    "data/UDP-testing.parquet",
    "data/DNS-testing.parquet",
    "data/LDAP-testing.parquet",
    "data/MSSQL-testing.parquet",
    "data/NetBIOS-testing.parquet",
    "data/NTP-testing.parquet",
    "data/SNMP-testing.parquet",
    "data/Syn-testing.parquet",
    "data/TFTP-testing.parquet",
    "data/UDPLag-testing.parquet"
]

dfs = []

for file in files:
    df = pd.read_parquet(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

print(combined_df["Label"].value_counts())

combined_df.to_parquet(
    "data/combined_dataset.parquet",
    index=False
)

print("Dataset Saved Successfully")
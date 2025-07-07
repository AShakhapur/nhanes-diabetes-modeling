import os
import requests
import pandas as pd

# NHANES 2017–2018 public CSV URLs
urls = {
    "DEMO_J.csv": "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.csv",
    "BMX_J.csv":  "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/BMX_J.csv",
    "GHB_J.csv":  "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/GHB_J.csv",
    "DIQ_J.csv":  "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DIQ_J.csv"
}

# Directory to save raw data
data_dir = "./datasets"
os.makedirs(data_dir, exist_ok=True)

# Step 1: Download .csv files
for filename, url in urls.items():
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        response = requests.get(url)
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Already exists: {filename}")

# Step 2: Load into DataFrames
dataframes = []
for filename in urls:
    path = os.path.join(data_dir, filename)
    df = pd.read_csv(path)
    df["SEQN"] = df["SEQN"].astype("Int64")  # Ensure merge key is consistent
    dataframes.append(df)
    print(f"Loaded: {filename} — Shape: {df.shape}")

    # Fix for corrupted small-float values in integer-like columns
    int_like_columns = ["DMDHHSZE", "DMDHHSZA", "DMDHHSZB", "DMDHHSIZ", "DMDFMSIZ"]

    for col in int_like_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].round().astype("Int64")



# Step 3: Merge all on SEQN
categorical_vars = [
    "RIAGENDR", "RIDRETH1", "RIDRETH3", "DMQMILIZ", "DMDBORN4", "DMDCITZN",
    "DMDEDUC2", "DMDMARTL", "DMDHHSIZ", "DMDFMSIZ", "DMDHHSZA", "DMDHHSZB",
    "DMDHHSZE", "INDHHIN2", "INDFMIN2"
]

merged = dataframes[0]
for df in dataframes[1:]:
    merged = pd.merge(merged, df, on="SEQN", how="left")

    for col in int_like_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].round().astype("Int64")

# Step 4: Save merged result
merged_path = os.path.join(data_dir, "nhanes_hba1c_merged.csv")
merged.to_csv(merged_path, index=False)
print(f"Merged dataset saved to: {merged_path}")
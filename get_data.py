import os
import requests
import pandas as pd

# URLs for NHANES 2017–2018 data components
urls = {
    "DEMO_J.XPT": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DEMO_J.xpt",   # Demographics
    "BMX_J.XPT":  "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BMX_J.xpt",    # Body Measures
    "GHB_J.XPT":  "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/GHB_J.xpt",    # HbA1C 
    "DIQ_J.XPT":  "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DIQ_J.xpt",    # Diabetes questionnaire
}


# Directory to save downloaded and processed files
data_dir = "./datasets"
os.makedirs(data_dir, exist_ok=True)

# Step 1: Download and save .xpt files
for filename, url in urls.items():
    xpt_path = os.path.join(data_dir, filename)
    if not os.path.exists(xpt_path):
        response = requests.get(url)
        with open(xpt_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Already exists: {filename}")

# Step 2: Convert .xpt files to .csv and load into DataFrames
dataframes = []
for file in urls.keys():
    xpt_path = os.path.join(data_dir, file)
    csv_path = xpt_path.replace(".XPT", ".csv")
    df = pd.read_sas(xpt_path, format="xport")
    df["SEQN"] = df["SEQN"].astype("Int64")  # enforce integer join key
    df.to_csv(csv_path, index=False)
    print(f"Converted: {file} -> {csv_path}")
    dataframes.append(df)

for i, df in enumerate(dataframes):
    print(f"\nDataFrame {i} shape: {df.shape}")
    print(df.head(2))
    print(df.isna().all().sum(), "columns with all NaN")
    print("Non-null counts per column:")
    print(df.notna().sum())



# Step 3: Merge all dataframes on SEQN
    # Assume the first df is DEMO_J
merged = dataframes[0]
for df in dataframes[1:]:
    merged = pd.merge(merged, df, on="SEQN", how="left")


# Step 4: Save merged file
merged_path = os.path.join(data_dir, "nhanes_hba1c_merged.csv")
merged.to_csv(merged_path, index=False)
print(f"Merged dataset saved to: {merged_path}")


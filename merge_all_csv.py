import pandas as pd
import os

folder = "datasets"
all_data = []

for file in os.listdir(folder):
    if file.endswith(".csv"):
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        df['Source File'] = file  # optional: to track origin
        all_data.append(df)

# Merge all CSVs into one
merged_df = pd.concat(all_data, ignore_index=True)
merged_df.to_csv("Merged_SalesData.csv", index=False)

print("✅ All CSV files merged into 'Merged_SalesData.csv'")

import pandas as pd
import numpy as np
import os

def run_ingestion():
    print("--- Starting Data Ingestion & Transformation ---")
    
    # Define file paths (adjust raw file paths as needed)
    raw_data_path = "data/raw_gdsc_fitted_dose_response.csv"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(raw_data_path):
        print(f"⚠️ Raw data file not found at {raw_data_path}. Skipping raw read.")
        return

    df = pd.read_csv(raw_data_path)
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Data Cleaning & Winsorization
    if 'ln_ic50' in df.columns:
        df = df.dropna(subset=['ln_ic50'])
        # Winsorize extreme outliers at 1st and 99th percentiles
        p1, p99 = np.percentile(df['ln_ic50'], [1, 99])
        df['ln_ic50'] = np.clip(df['ln_ic50'], p1, p99)

    # Save processed dataset
    df.to_csv(os.path.join(output_dir, "cleaned_drug_sensitivity.csv"), index=False)
    print("✅ Data Ingestion & Cleaning Complete.")

if __name__ == "__main__":
    run_ingestion()
import os
import time
import pandas as pd
from extract_data import automated_extraction

def run_data_quality_pipeline(df):
    print("\n==================================================")
    print(" STARTING ETL PIPELINE: STEP 2 (DATA QUALITY & TRANSFORM)")
    print("==================================================")
    
    if df is None:
        print(" Error: Received empty DataFrame.")
        return None

    start_time = time.time()
    
    # ----------------------------------------------------
    # 1. DATA CLEANING: Drop Structural Noise
    # ----------------------------------------------------
    print(" Cleaning structural noise...")
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        print("    Dropped 'Unnamed: 0' index artifact column.")

    # ----------------------------------------------------
    # 2. TRANSFORM: Convert String Timestamps to Datetime
    # ----------------------------------------------------
    print(" Converting transaction timestamps to database-optimized datetime...")
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    print("    Datetime transformation complete.")

    # ----------------------------------------------------
    # 3. FEATURE ENGINEERING: Apply Analyst Business Logic
    # ----------------------------------------------------
    print(" Applying Analyst Business Rule: Flagging High-Value Risks (> $1,000)...")
    df['high_value_risk'] = df['amt'].apply(lambda x: 1 if x > 1000 else 0)
    print("    High-value risk flags successfully baked into data stream.")

    # ----------------------------------------------------
    # 4. QUALITY LOGIC: Standard Anomaly Scans
    # ----------------------------------------------------
    print(" Scanning for duplicate rows or negative amounts...")
    anomalies_df = df[(df.duplicated()) | (df['amt'] <= 0)]
    total_anomalies = len(anomalies_df)
    
    # Isolate any historical anomalies to an audit file
    issue_file = "DQ_ISSUE.csv"
    if total_anomalies > 0:
        print(f" Warning: {total_anomalies} anomalies found. Isolating to '{issue_file}'")
        anomalies_df.to_csv(issue_file, index=False)
    else:
        if os.path.exists(issue_file):
            os.remove(issue_file)
        print("    Complete Check: Stream is clean of critical logical anomalies.")

    # Drop any exact duplicates to sanitize the final pipeline load
    clean_df = df.drop_duplicates()

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print("\n --- PRODUCTION PIPELINE METRICS ---")
    print(f" Total Processed Rows: {len(clean_df):,}")
    print(f" New Total Columns: {len(clean_df.columns)} (Includes 'high_value_risk')")
    print(f" Execution Time: {duration} seconds")
    print("==================================================\n")

    return clean_df

if __name__ == "__main__":
    # Ingest using your extraction script
    raw_data = automated_extraction()
    
    # Clean, transform, and feature engineer using your new rules!
    production_ready_data = run_data_quality_pipeline(raw_data)
    
    # Confirm the presence of the new column structure
    print(" Verifying production data stream columns:")
    print(production_ready_data[['trans_date_trans_time', 'amt', 'high_value_risk']].head(3))
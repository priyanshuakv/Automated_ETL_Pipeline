import pandas as pd
import numpy as np
import os
import kagglehub 

def run_production_data_quality_audit():
    print("\n==================================================")
    print(" STARTING PHASE 1: DYNAMIC DATA QUALITY AUDIT")
    print("==================================================")
    
    try:
        # 1. Ask kagglehub exactly where the files are cached on your system
        print(" Locating Kaggle dataset cache via kagglehub...")
        download_path = kagglehub.dataset_download("kartik2112/fraud-detection")
        csv_path = os.path.join(download_path, "fraudTrain.csv")
        
        if not os.path.exists(csv_path):
            print(f" Error: 'fraudTrain.csv' not found in cache path: {download_path}")
            return None
            
        print(f" Secure cache link verified: {download_path}")
        print(f" Ingesting live dataset: '{csv_path}'...")
        
        # 2. Ingest the data (Reading the actual cached file)
        df = pd.read_csv(csv_path)
        total_rows = len(df)
        print(f" Total raw records loaded from Kaggle cache: {total_rows:,} rows.")

    except Exception as e:
        print(f" Critical error accessing Kaggle cache stream: {e}")
        return None

    # =========================================================================
    # 🚨 DUMMY ANOMALY INJECTION FOR PIPELINE QUALITY & EMAIL TESTING
    # =========================================================================
    print(" [TESTING] Injecting synthetic data constraints for firewall validation...")
    if len(df) >= 10:
        # 1. Force a subset of rows to contain negative / zero values
        df.loc[df.index[0:3], 'amt'] = -150.75
        df.loc[df.index[3], 'amt'] = 0.00
        
        # 2. Force credit card number violations using np.nan (safe for float64/int64)
        df.loc[df.index[4:8], 'cc_num'] = np.nan
        
        # 3. Force missing merchant category classifications
        df.loc[df.index[8:10], 'category'] = np.nan
        print(f" [TESTING] Successfully injected {10} baseline data anomalies into stream.")
    # =========================================================================

    # 3. Vectorized Compliance Testing Masks (Scanning the data + injected issues!)
    print(" Auditing rows against business compliance rules...")
    bad_amt_mask = df['amt'] <= 0
    bad_cc_mask = df['cc_num'].isna() | (df['cc_num'].astype(str).str.strip() == '')
    bad_cat_mask = df['category'].isna() | (df['category'].astype(str).str.strip() == '')

    # 4. Process actual generated anomalies dynamically
    detected_issues = []
    anomaly_rows_amt = df[bad_amt_mask]
    anomaly_rows_cc = df[bad_cc_mask]
    anomaly_rows_cat = df[bad_cat_mask]

    print(" Compiling discovered anomalies into structural logs...")
    for idx, row in anomaly_rows_amt.iterrows():
        detected_issues.append({
            "transaction_id": row.get('trans_num', f"ROW_{idx}"),
            "error_type": "Negative/Zero Amount",
            "column_name": "amt",
            "invalid_value": row['amt'],
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    for idx, row in anomaly_rows_cc.iterrows():
        detected_issues.append({
            "transaction_id": row.get('trans_num', f"ROW_{idx}"),
            "error_type": "Missing Credit Card Number",
            "column_name": "cc_num",
            "invalid_value": "NULL/EMPTY",
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    for idx, row in anomaly_rows_cat.iterrows():
        detected_issues.append({
            "transaction_id": row.get('trans_num', f"ROW_{idx}"),
            "error_type": "Missing Category Classification",
            "column_name": "category",
            "invalid_value": "NULL",
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # 5. Filter out corrupt records to keep your future DB steps pristine
    all_bad_indices = df[bad_amt_mask | bad_cc_mask | bad_cat_mask].index
    clean_pipeline_df = df.drop(index=all_bad_indices)

    # 6. Save the actual generated anomalies to your workspace folder
    if detected_issues:
        dq_df = pd.DataFrame(detected_issues)
        dq_df.to_csv("DQ_ISSUE.csv", index=False)
        print(f" Data Quality Alert: Found {len(dq_df):,} anomalies in this batch!")
        print(" Real error ledger successfully compiled into local workspace: 'DQ_ISSUE.csv'")
    else:
        print(" Outstanding! 0 true structural anomalies found in this data batch.")
        if os.path.exists("DQ_ISSUE.csv"):
            os.remove("DQ_ISSUE.csv")

    print(f"✨ Clean Dataset Prepared: {len(clean_pipeline_df):,} rows isolated for loading.")
    print("==================================================\n")
    
    return clean_pipeline_df

if __name__ == "__main__":
    clean_df = run_production_data_quality_audit()
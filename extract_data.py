import os
import sys
import time
import kagglehub
import pandas as pd

def automated_extraction():
    print("\n==================================================")
    print(" STARTING ETL PIPELINE: STEP 1 (EXTRACTION)")
    print("==================================================")
    
    # 1. Verify Authentication Token Exists First
    user_profile = os.environ.get('USERPROFILE') or os.environ.get('HOME')
    token_path = os.path.join(user_profile, '.kaggle', 'access_token')
    
    print(f" Checking Kaggle authentication key at: {token_path}")
    if not os.path.exists(token_path):
        print(" CRITICAL ERROR: 'access_token' file not found inside your .kaggle folder!")
        print("Please review your token setup steps before running this script.")
        return None
    print(" Authentication key found successfully!")

    # 2. Trigger Download
    print("\n Connecting to Kaggle API servers...")
    print(" Downloading 'kartik2112/fraud-detection' (approx. 200MB)...")
    print(" NOTE: Terminal will pause here while data streams. Do not close VS Code!")
    
    start_time = time.time()
    
    try:
        # Download files via API cache
        download_path = kagglehub.dataset_download("kartik2112/fraud-detection")
        print(f"\n Download Complete! Files cached at: {download_path}")
        
        # 3. Locate Target CSV File
        csv_path = os.path.join(download_path, "fraudTrain.csv")
        if not os.path.exists(csv_path):
            print(f" Error: 'fraudTrain.csv' not found inside downloaded folder path: {download_path}")
            return None
            
        # 4. Ingest to Pandas Dataframe
        print(" Ingesting records into memory via Pandas DataFrame...")
        df = pd.read_csv(csv_path)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        print("\n --- EXTRACTION METRICS ---")
        print(f" Total Rows Loaded: {len(df):,}")
        print(f" Total Columns: {len(df.columns)}")
        print(f" Total Execution Time: {duration} seconds")
        print("==================================================\n")
        
        return df

    except Exception as e:
        print(f"\n Extraction failed due to an unexpected error: {e}")
        return None

# CRUCIAL: Ensure this line has absolutely ZERO spaces/tabs before it!
if __name__ == "__main__":
    raw_dataframe = automated_extraction()
    
    if raw_dataframe is not None:
        print(" Previewing live data stream structure:")
        print(raw_dataframe[['trans_date_trans_time', 'cc_num', 'merchant', 'amt']].head(5))
    else:
        print(" Pipeline stopped early because extraction failed.")
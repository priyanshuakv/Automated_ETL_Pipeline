import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

def load_clean_data_to_postgres(clean_dataframe):
    print("\n==================================================")
    print(" STARTING PHASE 2: INCREMENTAL DATABASE LOAD")
    print("==================================================")
    
    if clean_dataframe is None or clean_dataframe.empty:
        print(" No data package discovered for ingestion. Process halted.")
        return

    # Connection parameters to tie back to your database instance
    db_config = {
        "dbname": "FinGuard_DB",
        "user": "postgres",
        "password": os.getenv("DB_PASSWORD"), 
        "host": "localhost",
        "port": "5432"
    }

    try:
        print(" Linking connection pool to FinGuard_DB...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Explicit column structure mapping
        columns = [
            'trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt',
            'first', 'last', 'gender', 'street', 'city', 'state', 'zip',
            'lat', 'long', 'city_pop', 'job', 'dob', 'trans_num', 'unix_time',
            'merch_lat', 'merch_long', 'is_fraud'
        ]
        
        # Isolate clean values matrix
        data_to_insert = clean_dataframe[columns].values.tolist()
        total_records = len(data_to_insert)
        
        # Upsert rule logic: ON CONFLICT DO NOTHING tells postgres to skip duplicates safely
        insert_query = """
            INSERT INTO final_transactions (
                trans_date_trans_time, cc_num, merchant, category, amt,
                first_name, last_name, gender, street, city, state, zip,
                lat, long, city_pop, job, dob, trans_num, unix_time,
                merch_lat, merch_long, is_fraud
            ) VALUES %s
            ON CONFLICT (trans_num) DO NOTHING;
        """
        
        print(f" Pushing {total_records:,} verified transactions into production storage...")
        start_time = time.time()
        
        # Stream rows using fast batch execution tool
        execute_values(cursor, insert_query, data_to_insert)
        
        conn.commit()
        print(f" Ingestion successful! Batch processed in {time.time() - start_time:.2f} seconds.")
        
    except Exception as e:
        print(f" Database transaction rolled back due to error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print(" Connection line closed safely.")
    print("==================================================\n")

if __name__ == "__main__":
    # Link backwards to pull data directly from your phase 1 quality framework script
    from Financial_data_anomalies_Check import run_production_data_quality_audit
    
    # Run audit framework to isolate the clean dataframe batch
    clean_df_batch = run_production_data_quality_audit()
    
    # Push clean rows straight into postgres storage shelf
    load_clean_data_to_postgres(clean_df_batch)
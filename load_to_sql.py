import time
import psycopg2
import pandas as pd
from data_quality_checks import run_data_quality_pipeline
from extract_data import automated_extraction
import os
from dotenv import load_dotenv

load_dotenv()

def load_data_to_postgres(df):
    """
    STEP 3: LOAD TO STORAGE (POSTGRESQL VERSION)
    Pushes the polished, feature-engineered data straight into PostgreSQL.
    """
    print("\n==================================================")
    print(" STARTING ETL PIPELINE: STEP 3 (POSTGRESQL LOAD)")
    print("==================================================")
    
    if df is None:
        print(" Error: No data received for loading. Halting.")
        return

    # POSTGRESQL CONNECTION CONFIGURATION
    connection_config = {
        "dbname": "FinGuard_DB",
        "user": "postgres",
        "password": os.getenv("DB_PASSWORD"),  
        "host": "localhost",
        "port": "5432"
    }
    
    try:
        print(" Connecting to PostgreSQL Database...")
        conn = psycopg2.connect(**connection_config)
        cursor = conn.cursor()
        print("   Connection established successfully.")
        
        print("Mucking old records... Clearing previous data to prevent inflation...")
        cursor.execute("TRUNCATE TABLE final_transactions;")
        
        # Prepare the Postgres Insert Statement (Uses %s instead of ?)
        insert_query = """
        INSERT INTO final_transactions (
            trans_date_trans_time, cc_num, merchant, category, amt, 
            first_name, last_name, gender, street, city, state, zip, 
            lat, long, city_pop, job, dob, trans_num, unix_time, 
            merch_lat, merch_long, is_fraud, high_value_risk
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        print(" Preparing records for high-speed database ingestion...")
        # Ensure datetimes are strings for cleaner database translation
        df['trans_date_trans_time'] = df['trans_date_trans_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        records = df.values.tolist()
        
        print(f" Pumping {len(records):,} rows into PostgreSQL...")
        start_time = time.time()
        
        # Execute the bulk load safely in optimized chunks of 50,000 rows
        batch_size = 50000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            cursor.executemany(insert_query, batch)
            conn.commit() # Commit the batch to free up memory
            print(f"   📈 Saved rows {i:,} to {min(i + batch_size, len(records)):,}")
            
        end_time = time.time()
        print("\n --- DATABASE INGESTION METRICS ---")
        print(f" Data successfully loaded into PostgreSQL 'final_transactions' table!")
        print(f" database Load Time: {round(end_time - start_time, 2)} seconds")
        print("==================================================\n")
        
    except Exception as e:
        print(f" CRITICAL DATABASE LOAD ERROR: {e}")
        if 'conn' in locals():
            conn.rollback() 
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print(" PostgreSQL database connection securely closed.")

if __name__ == "__main__":
    print(" Triggering end-to-end automated pipeline...")
    # The chain reaction kicks off completely!
    raw_data = automated_extraction()
    clean_data = run_data_quality_pipeline(raw_data)
    
    # Run the Postgres database load
    load_data_to_postgres(clean_data)
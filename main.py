import os
import sys
import time

def run_entire_etl_pipeline():
    print("==================================================================")
    print(" FINGUARD AUTOMATED FINANCIAL ETL & DATA QUALITY PIPELINE 🌟")
    print("==================================================================")
    start_total_time = time.time()

    #  STEP 1: RUN DATA QUALITY AUDIT & EXTRACTION
    try:
        from Financial_data_anomalies_Check import run_production_data_quality_audit
        clean_df = run_production_data_quality_audit()
        
        if clean_df is None:
            print(" Pipeline Terminated: Extraction or Data Quality validation failed.")
            return
    except Exception as e:
        print(f" Critical Failure during Phase 1 (Data Quality Audit): {e}")
        return

    #  STEP 2: INCREMENTAL LOAD TO POSTGRESQL
    try:
        from load_clean_data import load_clean_data_to_postgres
        load_clean_data_to_postgres(clean_df)
    except Exception as e:
        print(f" Critical Failure during Phase 2 (Database Loading): {e}")
        print(" Pipeline frozen to protect database state. Notification email will not contain update summaries.")
        return

    #  STEP 3: EXECUTE EXECUTIVE PERFORMANCE METRICS & EMAIL DELIVERY
    try:
        print("\n==================================================")
        print(" STARTING PHASE 3: AUTOMATED STAKEHOLDER REPORTING")
        print("==================================================")
        print(" Querying database metrics and compiling HTML tables...")
        
        # Execute existing email script
        os.system("python send_email.py")
        
    except Exception as e:
        print(f" Failure during Phase 3 (Email Reporting Layer): {e}")

    #  SYSTEM SUMMARY LOGS
    total_duration = time.time() - start_total_time
    print("\n==================================================================")
    print(f" END-TO-END WORKFLOW EXECUTED SUCCESSFULY IN {total_duration:.2f} SECONDS")
    print("==================================================================")

if __name__ == "__main__":
    run_entire_etl_pipeline()
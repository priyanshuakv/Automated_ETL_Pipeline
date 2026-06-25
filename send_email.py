import os
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()


def generate_analytical_report():
    """
    Connects to Postgres, runs your optimized queries with LIMIT clauses,
    and formats them into a clean HTML email report.
    """
    print("\n==================================================")
    print(" GENERATING MONTHLY EXECUTIVE PERFORMANCE REPORT")
    print("==================================================")
    
    connection_config = {
        "dbname": "FinGuard_DB",
        "user": "postgres",
        "password": os.getenv("DB_PASSWORD"),  
        "host": "localhost",
        "port": "5432"
    }
    
    try:
        conn = psycopg2.connect(**connection_config)
        cursor = conn.cursor()
        
        # --- QUERY 1: TOP 3 FRAUD CATEGORIES ---
        cursor.execute("""
            SELECT category, COUNT(*), SUM(is_fraud), 
                   ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2)
            FROM final_transactions
            GROUP BY category
            ORDER BY sum(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END) DESC
            LIMIT 3;
        """)
        top_categories = cursor.fetchall()
        
        # --- QUERY 2: TOP 3 PEAK FRAUD HOURS ---
        cursor.execute("""
            SELECT EXTRACT(HOUR FROM trans_date_trans_time) as hr, COUNT(*), SUM(is_fraud),
                   ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2)
            FROM final_transactions
            GROUP BY EXTRACT(HOUR FROM trans_date_trans_time)
            ORDER BY sum(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END) DESC
            LIMIT 3;
        """)
        top_hours = cursor.fetchall()
        
        print(" Data successfully summarized for executive delivery.")
        return top_categories, top_hours
        
    except Exception as e:
        print(f" Error compiling report metrics: {e}")
        return None, None
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def send_executive_email_with_attachment(categories, hours, csv_filepath="DQ_ISSUE.csv"):
    """
    Constructs the HTML body and attaches a full CSV data quality report 
    for the technical team to review.
    """
    if not categories or not hours:
        return
        
    # --- CONFIGURATION SETTINGS ---
    sender_email = "priyanshuakv@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")  
    receiver_email = "vermaas221402@gmail.com"
    
    msg = MIMEMultipart() # Using default multipart to allow attachments smoothly
    msg['Subject'] = "🚨 Alert: Monthly Data Quality Audit & Financial Risk Report"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
   # --- HTML EMAIL TEMPLATE ---
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <h2 style="color: #d9534f;"> FinGuard Automated Risk Summary</h2>
        <p>Hello Team,</p>
        <p>Here is the monthly update of data quality checks and transaction risk anomalies captured during our automated ingestion window. The core data pipeline executed successfully, and the processed records have been fully reconciled into production storage.</p>
        <p>Please find the detailed data quality ledger attached (<code>DQ_ISSUE.csv</code>) highlighting specific structural breaks and high-exposure threshold alerts that require immediate operational review.</p>
        
        <hr style="border: 0; border-top: 1px solid #eee;">
        
        <h3> Top 3 High-Loss Merchant Sectors</h3>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; border-color: #ddd;">
          <tr style="background-color: #f8f9fa;">
            <th>Category</th><th>Total Swipes</th><th>Fraud Volume</th><th>Total Capital Loss</th>
          </tr>
          {"".join([f"<tr><td>{c[0]}</td><td>{c[1]:,}</td><td>{c[2]:,}</td><td>${float(c[3]):,.2f}</td></tr>" for c in categories])}
        </table>
        
        <h3> Top 3 Vulnerability Strike Hours</h3>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; border-color: #ddd;">
          <tr style="background-color: #f8f9fa;">
            <th>Hour of Day</th><th>Total Swipes</th><th>Fraud Volume</th><th>Total Capital Loss</th>
          </tr>
          {"".join([f"<tr><td>{int(h[0])}:00</td><td>{h[1]:,}</td><td>{h[2]:,}</td><td>${float(h[3]):,.2f}</td></tr>" for h in hours])}
        </table>
        
        <br>
        <p>Regards,<br>
        <strong>Priyanshu Verma</strong><br>
        <span style="font-size: 13px; color: #555;">Data Analyst | Risk Operations Tier</span></p>
        
        <hr style="border: 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #777;">🤖 <i>This is an automated operational intelligence report triggered directly by the FinGuard Python Backend.</i></p>
      </body>
    </html>
    """
    
    # Attach HTML text body
    msg.attach(MIMEText(html_content, 'html'))
    
    #  --- ATTACHING THE FULL REPORT CSV ---
    if os.path.exists(csv_filepath):
        print(f" Locating full audit file: {csv_filepath}")
        with open(csv_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(csv_filepath)}",
        )
        msg.attach(part)
        print("    Full report attached successfully.")
    else:
        print(" No separate anomaly CSV found. Sending summary text email only.")

    # --- SMTP TRANSMISSION ENGINE ---
    try:
        print(" Establishing secure SMTP email server connection...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        print(f" Dispatching summary directly to: {receiver_email}")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(" Email with attachment sent successfully!\n")
    except Exception as e:
        print(f" Failed to dispatch automated report (Check credentials/SMTP setup): {e}")

if __name__ == "__main__":
    cat_data, hr_data = generate_analytical_report()
    
    # Run the email sender, pointing to your local data anomalies spreadsheet file
    send_executive_email_with_attachment(cat_data, hr_data, csv_filepath="DQ_ISSUE.csv")
CREATE TABLE IF NOT EXISTS final_transactions (
    index SERIAL,
    trans_date_trans_time TIMESTAMP,
    cc_num BIGINT,
    merchant VARCHAR(255),
    category VARCHAR(100),
    amt NUMERIC(10, 2),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(10),
    street VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    zip INT,
    lat NUMERIC(10, 6),
    long NUMERIC(10, 6),
    city_pop INT,
    job VARCHAR(255),
    dob DATE,
    trans_num VARCHAR(100) PRIMARY KEY, -- 👈 This guards against duplicate rows!
    unix_time BIGINT,
    merch_lat NUMERIC(10, 6),
    merch_long NUMERIC(10, 6),
    is_fraud INT
);

-- Optimize query speeds for your monthly analytical loops
CREATE INDEX IF NOT EXISTS idx_trans_time ON final_transactions(trans_date_trans_time);


-- 1. Which merchant categories experience the highest frequency and volume of fraud?	
--To recommend which merchant types need stricter security authentication (like 2-Factor Authentication).
-- Query 1: Fraud Breakdown by Merchant Category
SELECT 
    category,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS total_fraud_cases,
    ROUND((SUM(is_fraud)::NUMERIC / COUNT(*)) * 100, 2) AS fraud_rate_percentage,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) AS total_stolen_amount
FROM final_transactions
GROUP BY category
ORDER BY total_stolen_amount DESC;

-- 2. What hour of the day is the most dangerous for fraudulent attacks?	
-- To help the IT team optimize real-time monitoring alerts during peak fraud hours.
-- Query 2: Identifying Peak Fraud Hours
SELECT 
    EXTRACT(HOUR FROM trans_date_trans_time) AS transaction_hour,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS total_fraud_cases,
    ROUND((SUM(is_fraud)::NUMERIC / COUNT(*)) * 100, 2) AS fraud_rate_percentage,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) AS total_stolen_amount
FROM final_transactions
GROUP BY EXTRACT(HOUR FROM trans_date_trans_time)
ORDER BY total_stolen_amount DESC;

-- 3. Are certain states or cities disproportionately targeted by fraudsters?	
-- To identify geographic fraud rings and update regional risk scores.
-- Query 3: Top States by Total Fraud Volume and Rates

SELECT 
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS total_fraud_cases,
    ROUND((SUM(is_fraud)::NUMERIC / COUNT(*)) * 100, 2) AS fraud_rate_percentage,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) AS total_stolen_amount
FROM final_transactions
GROUP BY state
ORDER BY total_stolen_amount DESC
LIMIT 5;

-- 4. Does a customer's gender or city population size correlate with higher fraud rates?	
-- To understand demographic vulnerability and build better user profiles.
-- Query 4: Fraud Inversion across Demographics (Gender)
SELECT 
    gender,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS total_fraud_cases,
    ROUND((SUM(is_fraud)::NUMERIC / COUNT(*)) * 100, 2) AS fraud_rate_percentage,
    ROUND(AVG(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) AS avg_fraudulent_ticket_size,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) AS total_stolen_amount
FROM final_transactions
GROUP BY gender;

-- 5. How much total money did our custom high_value_risk flag catch?	
-- To mathematically prove to your manager how effective your new rule is at saving company capital! 
-- Query 5: Measuring the Financial Impact of the High-Value Risk Flag
SELECT 
    high_value_risk,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS total_fraud_cases,
    ROUND((SUM(is_fraud)::NUMERIC / COUNT(*)) * 100, 2) AS fraud_rate_percentage,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) AS total_stolen_amount
FROM final_transactions
GROUP BY high_value_risk;

--6. The Business Question: Are fraudsters stealing larger amounts per transaction compared to legitimate shoppers?
SELECT 
    is_fraud,
    COUNT(*) as total_transactions,
    ROUND(AVG(amt), 2) as avg_transaction_amount,
    ROUND(MAX(amt), 2) as max_transaction_amount
FROM final_transactions
GROUP BY is_fraud;

--7. The Business Question: Are younger users or elderly users more vulnerable to financial fraud scams?
SELECT 
    CASE 
        WHEN EXTRACT(YEAR FROM AGE(trans_date_trans_time, dob)) < 30 THEN 'Under 30'
        WHEN EXTRACT(YEAR FROM AGE(trans_date_trans_time, dob)) BETWEEN 30 AND 50 THEN '30 - 50'
        ELSE 'Over 50'
    END as age_group,
    SUM(is_fraud) as fraud_incidents,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amt ELSE 0 END), 2) as total_fraud_loss
FROM final_transactions
GROUP BY age_group
ORDER BY fraud_incidents DESC;
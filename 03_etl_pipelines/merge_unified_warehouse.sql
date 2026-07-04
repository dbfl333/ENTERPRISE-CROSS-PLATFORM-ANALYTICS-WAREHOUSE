-- Merge all clean tenant tables and build a unified analytical warehouse schema
-- Output database: 04_clean_data/analytics_production.duckdb

-- 1. Create Dimension Tables

-- Property Dimension (Tenant C)
CREATE OR REPLACE TABLE dim_properties AS
SELECT 'PROP_01' AS property_id, 'Terrazas Ocean View' AS property_name, 250.00 AS base_rate UNION ALL
SELECT 'PROP_02', 'Terrazas Mountain Retreat', 180.00 UNION ALL
SELECT 'PROP_03', 'Terrazas Forest Cabin', 120.00 UNION ALL
SELECT 'PROP_04', 'Terrazas City Penthouse', 300.00 UNION ALL
SELECT 'PROP_05', 'Terrazas Desert Oasis', 150.00;

-- User Dimension (Tenant A)
CREATE OR REPLACE TABLE dim_users AS
SELECT DISTINCT 
    user_id,
    'User_' || SUBSTR(user_id, 1, 8) AS user_name
FROM clean_shop_sessions
WHERE user_id IS NOT NULL;

-- Asset Dimension (Tenant D)
CREATE OR REPLACE TABLE dim_assets AS
SELECT DISTINCT 
    asset_pair,
    CASE 
        WHEN asset_pair IN ('BTCUSD', 'ETHUSD', 'SOLUSD') THEN 'Cryptocurrency'
        WHEN asset_pair IN ('EURUSD') THEN 'Forex'
        ELSE 'Equity'
    END AS asset_class
FROM read_csv_auto('02_raw_data/gtrend_raw_backtests.csv');

-- Date Dimension (Shared)
CREATE OR REPLACE TABLE dim_dates AS
WITH RECURSIVE date_range AS (
    SELECT CAST('2025-01-01' AS DATE) AS date_day
    UNION ALL
    SELECT date_day + INTERVAL 1 DAY
    FROM date_range
    WHERE date_day < CAST('2027-12-31' AS DATE)
)
SELECT
    date_day AS date_key,
    YEAR(date_day) AS year,
    MONTH(date_day) AS month,
    MONTHNAME(date_day) AS month_name,
    DAY(date_day) AS day,
    DAYOFWEEK(date_day) AS day_of_week,
    DAYNAME(date_day) AS day_name,
    QUARTER(date_day) AS quarter
FROM date_range;


-- 2. Create Fact Tables

-- Fact Shop Sessions (Tenant A)
CREATE OR REPLACE TABLE fact_shop_sessions AS
SELECT
    session_id,
    user_id,
    event_timestamp,
    CAST(event_timestamp AS DATE) AS date_key,
    funnel_stage,
    price,
    country,
    device_type
FROM clean_shop_sessions;

-- Fact Prompt Telemetry (Tenant B)
CREATE OR REPLACE TABLE fact_prompt_telemetry AS
SELECT
    request_id,
    log_timestamp,
    CAST(log_timestamp AS DATE) AS date_key,
    prompt_token_count,
    completion_token_count,
    prompt_token_count + completion_token_count AS total_token_count,
    latency_ms,
    is_latency_outlier,
    http_status_code,
    agent_sub_routine,
    model,
    temperature
FROM clean_prompt_telemetry;

-- Fact Terrazas Bookings (Tenant C)
CREATE OR REPLACE TABLE fact_terrazas_bookings AS
SELECT
    booking_id,
    guest_name,
    property_id,
    created_at,
    check_in,
    check_out,
    nights,
    raw_amount,
    total_amount,
    status,
    is_double_booked
FROM clean_terrazas_bookings;

-- Fact G-Trend Quantitative Trades (Tenant D)
CREATE OR REPLACE TABLE fact_gtrend_trades AS
SELECT
    trade_id,
    asset_pair,
    CAST(entry_timestamp AS TIMESTAMP) AS entry_timestamp,
    CAST(exit_timestamp AS TIMESTAMP) AS exit_timestamp,
    CAST(entry_timestamp AS DATE) AS entry_date_key,
    position_type_long_short AS position_type,
    CAST(profit_loss_percentage AS DOUBLE) AS profit_loss_percentage,
    CAST(max_drawdown_percentage AS DOUBLE) AS max_drawdown_percentage,
    DATEDIFF('minute', CAST(entry_timestamp AS TIMESTAMP), CAST(exit_timestamp AS TIMESTAMP)) / 60.0 AS duration_hours
FROM read_csv_auto('02_raw_data/gtrend_raw_backtests.csv');


-- 3. Cleanup Temporary Working Tables
DROP TABLE clean_shop_sessions;
DROP TABLE clean_prompt_telemetry;
DROP TABLE clean_terrazas_bookings;

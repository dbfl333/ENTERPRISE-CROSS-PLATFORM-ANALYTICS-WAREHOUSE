-- Merge all clean tables and build the final star schema relational warehouse
-- Output database: 04_clean_data/analytics_production.duckdb

-- 1. Create Staging Schemas for Pre-launch Systems (Empty Staging Architecture)

-- Agentic Prompt Labs Staging Schema (Tenant C)
CREATE TABLE IF NOT EXISTS staging_prompt_telemetry (
    request_id VARCHAR PRIMARY KEY,
    agent_id VARCHAR,
    prompt_tokens INT,
    completion_tokens INT,
    latency_ms INT,
    http_status INT,
    execution_timestamp TIMESTAMP
);

-- Terrazas-home Staging Schema (Tenant D)
CREATE TABLE IF NOT EXISTS staging_terrazas_bookings (
    booking_id VARCHAR PRIMARY KEY,
    property_id VARCHAR,
    check_in DATE,
    check_out DATE,
    total_amount DECIMAL(10, 2),
    status VARCHAR,
    created_at TIMESTAMP
);


-- 2. Create Dimension Tables

-- User Dimension (derived from Shopify Customer emails)
CREATE OR REPLACE TABLE dim_users AS
SELECT DISTINCT 
    MD5(customer_email) AS user_key,
    customer_email AS email_address,
    SUBSTRING(customer_email FROM POSITION('@' IN customer_email) + 1) AS email_domain
FROM clean_shop_orders;

-- Asset Dimension (Binance BTC pair metadata)
CREATE OR REPLACE TABLE dim_assets AS
SELECT 
    'BTCUSDT' AS asset_pair,
    'Bitcoin / Tether USD' AS asset_name,
    'Cryptocurrency' AS asset_class;

-- Date Dimension (Shared Calendar)
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


-- 3. Create Fact Tables

-- Fact Shop Orders (Tenant A)
CREATE OR REPLACE TABLE fact_shop_orders AS
SELECT
    order_id,
    MD5(customer_email) AS user_key,
    total_amount,
    currency,
    order_timestamp,
    CAST(order_timestamp AS DATE) AS date_key,
    financial_status
FROM clean_shop_orders;

-- Fact Binance Klines (Tenant B)
CREATE OR REPLACE TABLE fact_binance_klines AS
SELECT
    open_timestamp,
    CAST(open_timestamp AS DATE) AS date_key,
    'BTCUSDT' AS asset_pair,
    open_price,
    high_price,
    low_price,
    close_price,
    trade_volume,
    close_timestamp,
    total_trades
FROM clean_binance_btc;


-- 4. Cleanup Working Temporary Tables
DROP TABLE clean_shop_orders;
DROP TABLE clean_binance_btc;

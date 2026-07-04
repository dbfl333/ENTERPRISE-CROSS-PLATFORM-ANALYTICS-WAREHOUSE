-- Merge all clean tables and build the final star schema relational warehouse
-- Output database: 04_clean_data/analytics_production.duckdb

-- 1. Create Staging Schemas for Pre-launch Systems (Empty Staging Architecture)

-- Agentic Prompt Labs Staging Schema (Tenant C)
CREATE OR REPLACE TABLE staging_prompt_telemetry AS
SELECT
    CAST(trend_id AS VARCHAR) AS trend_id,
    CAST(keyword_tracked AS VARCHAR) AS keyword_tracked,
    CAST(search_date AS TIMESTAMP) AS search_date,
    CAST(search_interest_score AS INTEGER) AS search_interest_score,
    CAST(geo_region AS VARCHAR) AS geo_region,
    CAST(platform_source AS VARCHAR) AS platform_source,
    CAST(top_related_query_1 AS VARCHAR) AS top_related_query_1,
    CAST(top_related_query_2 AS VARCHAR) AS top_related_query_2,
    CAST(top_related_query_3 AS VARCHAR) AS top_related_query_3,
    CAST(rising_query_1 AS VARCHAR) AS rising_query_1,
    CAST(rising_query_2 AS VARCHAR) AS rising_query_2,
    CAST(weekly_momentum_pct AS DOUBLE) AS weekly_momentum_pct,
    CAST(monthly_momentum_pct AS DOUBLE) AS monthly_momentum_pct,
    CAST(seasonality_index AS DOUBLE) AS seasonality_index,
    CAST(competition_level AS VARCHAR) AS competition_level,
    CAST(estimated_cpc_low AS DECIMAL(10,2)) AS estimated_cpc_low,
    CAST(estimated_cpc_high AS DECIMAL(10,2)) AS estimated_cpc_high,
    CAST(organic_difficulty AS INTEGER) AS organic_difficulty,
    CAST(search_volume_tier AS VARCHAR) AS search_volume_tier,
    CAST(profitable_niche_flag AS BOOLEAN) AS profitable_niche_flag
FROM read_csv_auto('02_raw_data/prompt_telemetry_staging.csv');


-- 2. Create Dimension Tables

-- User Dimension (derived from Shopify Customer data)
CREATE OR REPLACE TABLE dim_users AS
SELECT DISTINCT 
    MD5(customer_id) AS user_key,
    customer_id,
    customer_locale
FROM clean_shop_orders;

-- Asset Dimension (Binance multi-pair metadata)
CREATE OR REPLACE TABLE dim_assets AS
SELECT DISTINCT
    symbol AS asset_pair,
    CASE 
        WHEN symbol = 'BTCUSDT' THEN 'Bitcoin / Tether USD'
        WHEN symbol = 'ETHUSDT' THEN 'Ethereum / Tether USD'
        WHEN symbol = 'SOLUSDT' THEN 'Solana / Tether USD'
        ELSE symbol
    END AS asset_name,
    'Cryptocurrency' AS asset_class
FROM clean_binance_btc;

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
    checkout_id,
    MD5(customer_id) AS user_key,
    customer_id,
    customer_locale,
    referring_site,
    landing_site,
    abandoned_checkout_url,
    created_at,
    completed_at,
    CAST(created_at AS DATE) AS date_key,
    time_in_funnel_seconds,
    currency,
    subtotal_price,
    total_discounts,
    total_tax,
    total_price AS total_amount,
    financial_status,
    cart_token,
    device_type,
    browser_ip,
    buyer_accepts_marketing,
    cancel_reason
FROM clean_shop_orders;

-- Fact Binance Klines (Tenant B)
CREATE OR REPLACE TABLE fact_binance_klines AS
SELECT
    symbol,
    open_timestamp,
    close_timestamp,
    CAST(open_timestamp AS DATE) AS date_key,
    open_price,
    high_price,
    low_price,
    close_price,
    trade_volume AS trade_volume,
    quote_asset_volume,
    total_trades,
    taker_buy_base_volume,
    rsi_14,
    macd_line,
    macd_signal,
    sma_20,
    sma_50,
    daily_change_percent,
    volatility_index,
    timestamp_fetched,
    screener_good_pair_flag
FROM clean_binance_btc;


-- 4. Create GA4 Traffic & Session Staging Table (Tenant A — Google Analytics)
CREATE OR REPLACE TABLE staging_ga4_sessions AS
SELECT
    CAST(ROW_NUMBER() OVER () AS VARCHAR) AS record_id,
    CAST(session_date AS VARCHAR) AS session_date,
    CAST(session_source AS VARCHAR) AS session_source,
    CAST(session_medium AS VARCHAR) AS session_medium,
    CAST(campaign_name AS VARCHAR) AS campaign_name,
    CAST(landing_page AS VARCHAR) AS landing_page,
    CAST(country AS VARCHAR) AS country,
    CAST(device_category AS VARCHAR) AS device_category,
    CAST(operating_system AS VARCHAR) AS operating_system,
    CAST(browser AS VARCHAR) AS browser,
    CAST(sessions AS INTEGER) AS sessions,
    CAST(new_users AS INTEGER) AS new_users,
    CAST(bounce_rate AS DOUBLE) AS bounce_rate,
    CAST(avg_session_duration_sec AS DOUBLE) AS avg_session_duration_sec,
    CAST(page_views AS INTEGER) AS page_views,
    CAST(conversions AS INTEGER) AS conversions,
    CAST(total_revenue AS DECIMAL(10,2)) AS total_revenue,
    CAST(data_source AS VARCHAR) AS data_source,
    CAST(extraction_date AS VARCHAR) AS extraction_date
FROM read_csv_auto('02_raw_data/ga4_sessions.csv');


-- 5. Create Shopify Marketing Events Staging Table (Tenant A — Marketing Attribution)
CREATE OR REPLACE TABLE staging_shopify_marketing AS
SELECT
    CAST(event_id AS VARCHAR) AS event_id,
    CAST(started_at AS VARCHAR) AS started_at,
    CAST(ended_at AS VARCHAR) AS ended_at,
    CAST(scheduled_to_end AS VARCHAR) AS scheduled_to_end,
    CAST(budget AS DECIMAL(10,2)) AS budget,
    CAST(currency AS VARCHAR) AS currency,
    CAST(event_type AS VARCHAR) AS event_type,
    CAST(source AS VARCHAR) AS source,
    CAST(channel AS VARCHAR) AS channel,
    CAST(utm_source AS VARCHAR) AS utm_source,
    CAST(utm_medium AS VARCHAR) AS utm_medium,
    CAST(utm_campaign AS VARCHAR) AS utm_campaign,
    CAST(paid_budget_percent_used AS DOUBLE) AS paid_budget_percent_used,
    CAST(impressions AS INTEGER) AS impressions,
    CAST(clicks AS INTEGER) AS clicks,
    CAST(click_through_rate AS DOUBLE) AS click_through_rate,
    CAST(spend AS DECIMAL(10,2)) AS spend,
    CAST(conversions_attributed AS INTEGER) AS conversions_attributed,
    CAST(attributed_revenue AS DECIMAL(10,2)) AS attributed_revenue,
    CAST(roas AS DOUBLE) AS roas
FROM read_csv_auto('02_raw_data/shopify_marketing_events.csv');


-- 6. Cleanup Working Temporary Tables
DROP TABLE clean_shop_orders;
DROP TABLE clean_binance_btc;

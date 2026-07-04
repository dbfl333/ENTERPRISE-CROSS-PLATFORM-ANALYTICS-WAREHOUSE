-- Merge all clean tables and build the final star schema relational warehouse
-- Output database: 04_clean_data/analytics_production.duckdb

-- 1. Create Staging Schemas for Pre-launch Systems (Empty Staging Architecture)

-- Agentic Prompt Labs Staging Schema (Tenant C)
CREATE OR REPLACE TABLE staging_prompt_telemetry AS
WITH Telemetry AS (
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
    FROM read_csv_auto('02_raw_data/prompt_raw_telemetry.csv')
),
GitHub AS (
    SELECT
        CAST(name AS VARCHAR) AS top_github_repo,
        CAST(stargazers_count AS INTEGER) AS top_github_stars
    FROM read_csv_auto('02_raw_data/github_agent_demand_raw.csv')
    ORDER BY stargazers_count DESC
    LIMIT 1
),
ArXiv AS (
    SELECT
        CAST(title AS VARCHAR) AS latest_arxiv_title
    FROM read_csv_auto('02_raw_data/arxiv_academic_trends_raw.csv')
    LIMIT 1
),
HN AS (
    SELECT
        CAST(story_id AS VARCHAR) AS top_hn_story_id
    FROM read_csv_auto('02_raw_data/hackernews_tech_raw.csv')
    LIMIT 1
)
SELECT
    t.trend_id,
    t.keyword_tracked,
    t.search_date,
    t.search_interest_score,
    t.geo_region,
    t.platform_source,
    t.top_related_query_1,
    t.top_related_query_2,
    t.top_related_query_3,
    t.rising_query_1,
    t.rising_query_2,
    t.weekly_momentum_pct,
    t.monthly_momentum_pct,
    t.seasonality_index,
    t.competition_level,
    t.estimated_cpc_low,
    t.estimated_cpc_high,
    t.organic_difficulty,
    t.search_volume_tier,
    t.profitable_niche_flag,
    COALESCE(g.top_github_repo, 'unknown') AS top_github_repo,
    COALESCE(g.top_github_stars, 0) AS top_github_stars,
    COALESCE(a.latest_arxiv_title, 'unknown') AS latest_arxiv_title,
    COALESCE(h.top_hn_story_id, 'unknown') AS top_hn_story_id
FROM Telemetry t
CROSS JOIN GitHub g
CROSS JOIN ArXiv a
CROSS JOIN HN h;


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
    cancel_reason,
    rate_EUR,
    rate_GBP,
    rate_MXN,
    geo_country,
    geo_city,
    geo_latitude,
    geo_longitude,
    wiki_views
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
    fng_value,
    fng_classification,
    trending_coin_name,
    trending_coin_symbol,
    btc_hash_rate,
    btc_market_price_usd,
    timestamp_fetched,
    screener_good_pair_flag
FROM clean_binance_btc;


-- 4. Cleanup Working Temporary Tables
DROP TABLE clean_shop_orders;
DROP TABLE clean_binance_btc;

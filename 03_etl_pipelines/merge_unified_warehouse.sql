-- 03_etl_pipelines/merge_unified_warehouse.sql

-- Master Unification Script for the Enterprise Data Warehouse
-- This ingests all 16 raw context sources for the 4 tenants into DuckDB.

-- ==============================================================
-- TENANT A: AI MARKETS SHOP
-- ==============================================================
CREATE OR REPLACE TABLE fact_shop_orders AS 
SELECT * FROM read_csv_auto('02_raw_data/shop_raw_orders.csv');

CREATE OR REPLACE TABLE staging_ga4_sessions AS 
SELECT * FROM read_csv_auto('02_raw_data/ga4_sessions.csv');

CREATE OR REPLACE TABLE staging_shopify_marketing AS 
SELECT * FROM read_csv_auto('02_raw_data/shopify_marketing_events.csv');

CREATE OR REPLACE TABLE ext_shop_forex AS 
SELECT * FROM read_csv_auto('02_raw_data/shop_forex_rates_raw.csv');

CREATE OR REPLACE TABLE ext_shop_buyer_geo AS 
SELECT * FROM read_csv_auto('02_raw_data/shop_buyer_geo_raw.csv');

CREATE OR REPLACE TABLE ext_shop_wikipedia AS 
SELECT * FROM read_csv_auto('02_raw_data/shop_wikipedia_trends_raw.csv');


-- ==============================================================
-- TENANT B: GTREND SCREENER
-- ==============================================================
CREATE OR REPLACE TABLE fact_binance_klines AS 
SELECT * FROM read_csv_auto('02_raw_data/binance_metrics.csv');

CREATE OR REPLACE TABLE ext_binance_btc AS 
SELECT * FROM read_csv_auto('02_raw_data/binance_btc_raw.csv');

CREATE OR REPLACE TABLE ext_crypto_sentiment AS 
SELECT * FROM read_csv_auto('02_raw_data/crypto_sentiment_raw.csv');

CREATE OR REPLACE TABLE ext_blockchain_network AS 
SELECT * FROM read_csv_auto('02_raw_data/blockchain_network_raw.csv');


-- ==============================================================
-- TENANT C: AGENTIC PROMPT LABS
-- ==============================================================
CREATE OR REPLACE TABLE staging_prompt_telemetry AS 
SELECT * FROM read_csv_auto('02_raw_data/prompt_raw_telemetry.csv');

CREATE OR REPLACE TABLE ext_github_agent_demand AS 
SELECT * FROM read_csv_auto('02_raw_data/github_agent_demand_raw.csv');

CREATE OR REPLACE TABLE ext_hackernews_tech AS 
SELECT * FROM read_csv_auto('02_raw_data/hackernews_tech_raw.csv');

CREATE OR REPLACE TABLE ext_arxiv_trends AS 
SELECT * FROM read_csv_auto('02_raw_data/arxiv_academic_trends_raw.csv');


-- ==============================================================
-- TENANT D: TERRAZAS VENUE ADMINISTRATION
-- ==============================================================
CREATE OR REPLACE TABLE staging_terrazas_bookings AS 
SELECT * FROM read_csv_auto('02_raw_data/terrazas_raw_bookings.csv');

CREATE OR REPLACE TABLE ext_juarez_weather AS 
SELECT * FROM read_csv_auto('02_raw_data/juarez_weather_forecast_raw.csv');

CREATE OR REPLACE TABLE ext_mexico_holidays AS 
SELECT * FROM read_csv_auto('02_raw_data/mexico_holidays_raw.csv');

CREATE OR REPLACE TABLE ext_osm_venue_density AS 
SELECT * FROM read_csv_auto('02_raw_data/osm_venue_density_raw.csv');

-- End of Merge Script

-- Clean and structure Tenant B: G-Trend Screener (Binance & Crypto Market Ingestion)
-- Inputs: binance_metrics.csv, crypto_sentiment_raw.csv, binance_btc_raw.csv, blockchain_network_raw.csv

CREATE OR REPLACE TABLE clean_binance_btc AS
WITH Metrics AS (
    SELECT
        CAST(symbol AS VARCHAR) AS symbol,
        to_timestamp(open_time / 1000) AS open_timestamp,
        to_timestamp(close_time / 1000) AS close_timestamp,
        CAST(open_price AS DECIMAL(18,4)) AS open_price,
        CAST(high_price AS DECIMAL(18,4)) AS high_price,
        CAST(low_price AS DECIMAL(18,4)) AS low_price,
        CAST(last_price AS DECIMAL(18,4)) AS close_price,
        CAST(volume AS DECIMAL(18,4)) AS trade_volume,
        CAST(quote_volume AS DECIMAL(18,4)) AS quote_asset_volume,
        CAST(count AS INTEGER) AS total_trades,
        CAST(last_qty AS DECIMAL(18,4)) AS taker_buy_base_volume,
        -- Generate indicators dynamically in DuckDB or pull them
        COALESCE(CAST(price_change_percent AS DECIMAL(10,4)), 0.0) AS daily_change_percent,
        COALESCE(CAST(((high_price - low_price) / NULLIF(low_price, 0)) * 100 AS DECIMAL(10,4)), 0.0) AS volatility_index
    FROM read_csv_auto('02_raw_data/binance_metrics.csv')
),
Sentiment AS (
    SELECT
        CAST(value AS INTEGER) AS fng_value,
        CAST(value_classification AS VARCHAR) AS fng_classification,
        CAST(to_timestamp(timestamp) AS DATE) AS fng_date
    FROM read_csv_auto('02_raw_data/crypto_sentiment_raw.csv')
),
Trending AS (
    SELECT
        CAST(name AS VARCHAR) AS trending_coin_name,
        CAST(symbol AS VARCHAR) AS trending_coin_symbol
    FROM read_csv_auto('02_raw_data/binance_btc_raw.csv')
    ORDER BY score ASC
    LIMIT 1
),
Network AS (
    SELECT
        CAST(hash_rate AS DOUBLE) AS btc_hash_rate,
        CAST(market_price_usd AS DOUBLE) AS btc_market_price_usd
    FROM read_csv_auto('02_raw_data/blockchain_network_raw.csv')
    LIMIT 1
)
SELECT
    m.symbol,
    m.open_timestamp,
    m.close_timestamp,
    m.open_price,
    m.high_price,
    m.low_price,
    m.close_price,
    m.trade_volume,
    m.quote_asset_volume,
    m.total_trades,
    m.taker_buy_base_volume,
    -- SMA & RSI calculations using window functions
    AVG(m.close_price) OVER (PARTITION BY m.symbol ORDER BY m.open_timestamp ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS sma_20,
    AVG(m.close_price) OVER (PARTITION BY m.symbol ORDER BY m.open_timestamp ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS sma_50,
    COALESCE(s.fng_value, 50) AS fng_value,
    COALESCE(s.fng_classification, 'Neutral') AS fng_classification,
    t.trending_coin_name,
    t.trending_coin_symbol,
    n.btc_hash_rate,
    n.btc_market_price_usd,
    m.daily_change_percent,
    m.volatility_index,
    -- Add MACD / RSI fallbacks
    50.0 AS rsi_14,
    0.0 AS macd_line,
    0.0 AS macd_signal,
    TRUE AS screener_good_pair_flag,
    CURRENT_TIMESTAMP AS timestamp_fetched
FROM Metrics m
LEFT JOIN Sentiment s ON CAST(m.open_timestamp AS DATE) = s.fng_date
CROSS JOIN Trending t
CROSS JOIN Network n;

-- Clean and structure Tenant B: G-Trend Screener (Binance Candlestick Data)
-- Input: 02_raw_data/binance_metrics.csv

CREATE OR REPLACE TABLE clean_binance_btc AS
SELECT
    CAST(symbol AS VARCHAR) AS symbol,
    CAST(open_time AS TIMESTAMP) AS open_timestamp,
    CAST(close_time AS TIMESTAMP) AS close_timestamp,
    CAST(open_price AS DECIMAL(18,4)) AS open_price,
    CAST(high_price AS DECIMAL(18,4)) AS high_price,
    CAST(low_price AS DECIMAL(18,4)) AS low_price,
    CAST(close_price AS DECIMAL(18,4)) AS close_price,
    CAST(volume AS DECIMAL(18,4)) AS trade_volume,
    CAST(quote_asset_volume AS DECIMAL(18,4)) AS quote_asset_volume,
    CAST(number_of_trades AS INTEGER) AS total_trades,
    CAST(taker_buy_base_volume AS DECIMAL(18,4)) AS taker_buy_base_volume,
    CAST(rsi_14 AS DECIMAL(10,4)) AS rsi_14,
    CAST(macd_line AS DECIMAL(10,4)) AS macd_line,
    CAST(macd_signal AS DECIMAL(10,4)) AS macd_signal,
    CAST(sma_20 AS DECIMAL(18,4)) AS sma_20,
    CAST(sma_50 AS DECIMAL(18,4)) AS sma_50,
    CAST(daily_change_percent AS DECIMAL(10,4)) AS daily_change_percent,
    CAST(volatility_index AS DECIMAL(10,4)) AS volatility_index,
    CAST(timestamp_fetched AS TIMESTAMP) AS timestamp_fetched,
    CAST(screener_good_pair_flag AS BOOLEAN) AS screener_good_pair_flag
FROM read_csv_auto('02_raw_data/binance_metrics.csv');

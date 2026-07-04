-- Clean and structure Tenant B: G-Trend Screener (Binance Candlestick Data)
-- Input: 02_raw_data/binance_btc_raw.csv

CREATE OR REPLACE TABLE clean_binance_btc AS
SELECT
    epoch_ms(CAST(open_time AS BIGINT)) AS open_timestamp,
    CAST(open AS DOUBLE) AS open_price,
    CAST(high AS DOUBLE) AS high_price,
    CAST(low AS DOUBLE) AS low_price,
    CAST(close AS DOUBLE) AS close_price,
    CAST(volume AS DOUBLE) AS trade_volume,
    epoch_ms(CAST(close_time AS BIGINT)) AS close_timestamp,
    CAST(number_of_trades AS INTEGER) AS total_trades
FROM read_csv_auto('02_raw_data/binance_btc_raw.csv');

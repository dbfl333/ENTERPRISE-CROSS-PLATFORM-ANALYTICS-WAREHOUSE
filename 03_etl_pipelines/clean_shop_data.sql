-- Clean and structure Tenant A: AI Markets Shop (E-Commerce Performance Tracking)
-- Input: 02_raw_data/shop_raw_sessions.csv

CREATE OR REPLACE TABLE clean_shop_sessions AS
SELECT
    session_id,
    -- Handle missing user IDs on abandoned paths by casting empty strings to NULL
    NULLIF(user_id, '') AS user_id,
    -- Cast timestamp to standard ISO timestamp format
    CAST(timestamp AS TIMESTAMP) AS event_timestamp,
    funnel_stage,
    -- Normalize the pricing string formats (e.g. $150.00, 150, and 150,00 USD)
    CAST(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    COALESCE(NULLIF(price_string, ''), '0'), 
                    '\$', '', 'g'
                ), 
                ' USD', '', 'g'
            ), 
            ',', '.', 'g'
        ) AS DECIMAL(10, 2)
    ) AS price,
    -- Handle empty customer geographic fields
    COALESCE(NULLIF(country, ''), 'Unknown') AS country,
    device_type
FROM read_csv_auto('02_raw_data/shop_raw_sessions.csv');

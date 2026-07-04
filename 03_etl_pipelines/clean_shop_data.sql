-- Clean and structure Tenant A: AI Markets Shop (E-Commerce Ingestion)
-- Input: 02_raw_data/shop_raw_orders.csv

CREATE OR REPLACE TABLE clean_shop_orders AS
WITH ProcessedOrders AS (
    SELECT 
        CAST(id AS VARCHAR) AS order_id,
        COALESCE(LOWER(TRIM(email)), 'offline_checkout@domain.com') AS customer_email,
        CAST(total_price AS DECIMAL(10,2)) AS total_amount,
        COALESCE(currency, 'USD') AS currency,
        CAST(created_at AS TIMESTAMP) AS order_timestamp,
        COALESCE(financial_status, 'unknown') AS financial_status,
        -- Deduplicate if any duplicate ID is present in the raw data pull
        ROW_NUMBER() OVER(PARTITION BY id ORDER BY created_at DESC) as row_num
    FROM read_csv_auto('02_raw_data/shop_raw_orders.csv')
)
SELECT 
    order_id,
    customer_email,
    total_amount,
    currency,
    order_timestamp,
    financial_status
FROM ProcessedOrders 
WHERE row_num = 1;

-- Clean and structure Tenant A: AI Markets Shop (E-Commerce Ingestion)
-- Input: 02_raw_data/shop_raw_orders.csv

CREATE OR REPLACE TABLE clean_shop_orders AS
WITH ProcessedOrders AS (
    SELECT 
        CAST(checkout_id AS VARCHAR) AS checkout_id,
        CAST(customer_id AS VARCHAR) AS customer_id,
        COALESCE(customer_locale, 'en-US') AS customer_locale,
        CAST(referring_site AS VARCHAR) AS referring_site,
        CAST(landing_site AS VARCHAR) AS landing_site,
        CAST(abandoned_checkout_url AS VARCHAR) AS abandoned_checkout_url,
        CAST(created_at AS TIMESTAMP) AS created_at,
        TRY_CAST(completed_at AS TIMESTAMP) AS completed_at,
        CAST(time_in_funnel_seconds AS INTEGER) AS time_in_funnel_seconds,
        COALESCE(currency, 'USD') AS currency,
        CAST(subtotal_price AS DECIMAL(10,2)) AS subtotal_price,
        CAST(total_discounts AS DECIMAL(10,2)) AS total_discounts,
        CAST(total_tax AS DECIMAL(10,2)) AS total_tax,
        CAST(total_price AS DECIMAL(10,2)) AS total_price,
        COALESCE(financial_status, 'unknown') AS financial_status,
        CAST(cart_token AS VARCHAR) AS cart_token,
        COALESCE(device_type, 'unknown') AS device_type,
        CAST(browser_ip AS VARCHAR) AS browser_ip,
        CAST(buyer_accepts_marketing AS BOOLEAN) AS buyer_accepts_marketing,
        CAST(cancel_reason AS VARCHAR) AS cancel_reason,
        ROW_NUMBER() OVER(PARTITION BY checkout_id ORDER BY created_at DESC) as row_num
    FROM read_csv_auto('02_raw_data/shop_raw_orders.csv')
)
SELECT 
    checkout_id,
    customer_id,
    customer_locale,
    referring_site,
    landing_site,
    abandoned_checkout_url,
    created_at,
    completed_at,
    time_in_funnel_seconds,
    currency,
    subtotal_price,
    total_discounts,
    total_tax,
    total_price,
    financial_status,
    cart_token,
    device_type,
    browser_ip,
    buyer_accepts_marketing,
    cancel_reason
FROM ProcessedOrders 
WHERE row_num = 1;

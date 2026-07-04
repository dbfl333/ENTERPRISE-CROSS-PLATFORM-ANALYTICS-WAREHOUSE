-- Clean and structure Tenant A: AI Markets Shop (E-Commerce Ingestion)
-- Inputs: shop_raw_orders.csv, shop_forex_rates_raw.csv, shop_buyer_geo_raw.csv, shop_wikipedia_trends_raw.csv

CREATE OR REPLACE TABLE clean_shop_orders AS
WITH Orders AS (
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
),
Forex AS (
    SELECT 
        CAST(rate_EUR AS DOUBLE) AS rate_EUR,
        CAST(rate_GBP AS DOUBLE) AS rate_GBP,
        CAST(rate_MXN AS DOUBLE) AS rate_MXN
    FROM read_csv_auto('02_raw_data/shop_forex_rates_raw.csv')
    LIMIT 1
),
Geo AS (
    SELECT 
        CAST(country AS VARCHAR) AS geo_country,
        CAST(city AS VARCHAR) AS geo_city,
        CAST(latitude AS DOUBLE) AS geo_latitude,
        CAST(longitude AS DOUBLE) AS geo_longitude
    FROM read_csv_auto('02_raw_data/shop_buyer_geo_raw.csv')
    LIMIT 1
),
Wiki AS (
    SELECT 
        TRY_CAST(SUBSTRING(CAST(timestamp AS VARCHAR), 1, 8) AS DATE) AS wiki_date,
        CAST(views AS INTEGER) AS wiki_views
    FROM read_csv_auto('02_raw_data/shop_wikipedia_trends_raw.csv')
)
SELECT 
    o.checkout_id,
    o.customer_id,
    o.customer_locale,
    o.referring_site,
    o.landing_site,
    o.abandoned_checkout_url,
    o.created_at,
    o.completed_at,
    o.time_in_funnel_seconds,
    o.currency,
    o.subtotal_price,
    o.total_discounts,
    o.total_tax,
    o.total_price,
    o.financial_status,
    o.cart_token,
    o.device_type,
    o.browser_ip,
    o.buyer_accepts_marketing,
    o.cancel_reason,
    COALESCE(f.rate_EUR, 0.92) AS rate_EUR,
    COALESCE(f.rate_GBP, 0.78) AS rate_GBP,
    COALESCE(f.rate_MXN, 18.50) AS rate_MXN,
    COALESCE(g.geo_country, 'United States') AS geo_country,
    COALESCE(g.geo_city, 'Mountain View') AS geo_city,
    COALESCE(g.geo_latitude, 37.42) AS geo_latitude,
    COALESCE(g.geo_longitude, -122.08) AS geo_longitude,
    COALESCE(w.wiki_views, 1200) AS wiki_views
FROM Orders o
CROSS JOIN Forex f
CROSS JOIN Geo g
LEFT JOIN Wiki w ON CAST(o.created_at AS DATE) = w.wiki_date
WHERE o.row_num = 1;

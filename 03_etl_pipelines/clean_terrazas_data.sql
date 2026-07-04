-- Clean and structure Tenant C: Terrazas-home (Event Management & Property Bookings)
-- Input: 02_raw_data/terrazas_raw_bookings.csv

-- Helper view to normalize the messy date formats into standard dates
CREATE OR REPLACE TABLE clean_terrazas_bookings_pre AS
WITH parsed_dates AS (
    SELECT
        booking_id,
        guest_name,
        property_id,
        -- created_at parsing
        CASE 
            WHEN created_at LIKE '%-%-% %:%:%' THEN strptime(created_at, '%d-%m-%Y %H:%M:%S')
            ELSE CAST(created_at AS TIMESTAMP)
        END AS created_at,
        
        -- check_in parsing
        CASE 
            WHEN check_in LIKE '%/%/%' THEN strptime(check_in, '%m/%d/%Y')::DATE
            WHEN check_in SIMILAR TO '[0-9]{4}-[0-9]{2}-[0-9]{2}' THEN CAST(check_in AS DATE)
            ELSE 
                strptime(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(check_in, '^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s*', ''),
                            '([0-9]+)(st|nd|rd|th)', '\1'
                        ),
                        '\s+', ' '
                    ),
                    '%B %d, %Y'
                )::DATE
        END AS check_in,

        -- check_out parsing
        CASE 
            WHEN check_out LIKE '%/%/%' THEN strptime(check_out, '%m/%d/%Y')::DATE
            WHEN check_out SIMILAR TO '[0-9]{4}-[0-9]{2}-[0-9]{2}' THEN CAST(check_out AS DATE)
            ELSE 
                strptime(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(check_out, '^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s*', ''),
                            '([0-9]+)(st|nd|rd|th)', '\1'
                        ),
                        '\s+', ' '
                    ),
                    '%B %d, %Y'
                )::DATE
        END AS check_out,
        
        CAST(total_amount AS DECIMAL(10, 2)) AS raw_amount,
        status
    FROM read_csv_auto('02_raw_data/terrazas_raw_bookings.csv')
)
SELECT
    booking_id,
    guest_name,
    property_id,
    created_at,
    check_in,
    check_out,
    DATEDIFF('day', check_in, check_out) AS nights,
    raw_amount,
    -- Handle zero-dollar booking anomalies: recalculate base on standard rates
    CASE 
        WHEN raw_amount = 0.00 AND status != 'Cancelled' THEN
            CAST(
                (CASE property_id
                    WHEN 'PROP_01' THEN 250.00
                    WHEN 'PROP_02' THEN 180.00
                    WHEN 'PROP_03' THEN 120.00
                    WHEN 'PROP_04' THEN 300.00
                    WHEN 'PROP_05' THEN 150.00
                    ELSE 100.00
                END) * DATEDIFF('day', check_in, check_out) * 
                -- Apply summer seasonal multiplier 1.3x
                (CASE WHEN MONTH(check_in) IN (6, 7, 8) THEN 1.3 ELSE 1.0 END)
            AS DECIMAL(10, 2))
        ELSE raw_amount
    END AS total_amount,
    status
FROM parsed_dates;

-- Detect and flag double bookings
CREATE OR REPLACE TABLE clean_terrazas_bookings AS
SELECT
    t1.*,
    -- A booking is double booked if there is another booking for the same property
    -- whose dates overlap and neither is cancelled.
    EXISTS (
        SELECT 1 
        FROM clean_terrazas_bookings_pre t2
        WHERE t1.property_id = t2.property_id
          AND t1.booking_id != t2.booking_id
          AND t1.status != 'Cancelled'
          AND t2.status != 'Cancelled'
          AND t1.check_in < t2.check_out
          AND t2.check_in < t1.check_out
    ) AS is_double_booked
FROM clean_terrazas_bookings_pre t1;

DROP TABLE clean_terrazas_bookings_pre;

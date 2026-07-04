-- Clean and structure Tenant D: Terrazas-home (Venue Administration Platform)
-- Input: 02_raw_data/terrazas_bookings_staging.csv

CREATE OR REPLACE TABLE staging_terrazas_bookings AS
SELECT
    CAST(reservation_id AS VARCHAR) AS reservation_id,
    CAST(venue_id AS VARCHAR) AS venue_id,
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(event_type AS VARCHAR) AS event_type,
    CAST(check_in_timestamp AS TIMESTAMP) AS check_in_timestamp,
    CAST(check_out_timestamp AS TIMESTAMP) AS check_out_timestamp,
    CAST(total_hours_booked AS DOUBLE) AS total_hours_booked,
    CAST(base_venue_price AS DECIMAL(10,2)) AS base_venue_price,
    CAST(seasonal_multiplier AS DOUBLE) AS seasonal_multiplier,
    CAST(inventory_rentals_json AS VARCHAR) AS inventory_rentals_json,
    CAST(service_addons_json AS VARCHAR) AS service_addons_json,
    CAST(security_deposit_held AS DECIMAL(10,2)) AS security_deposit_held,
    CAST(cleaning_fee AS DECIMAL(10,2)) AS cleaning_fee,
    CAST(total_gross_amount AS DECIMAL(10,2)) AS total_gross_amount,
    CAST(payment_status AS VARCHAR) AS payment_status,
    CAST(contract_signed_status AS BOOLEAN) AS contract_signed_status,
    CAST(cancellation_policy_type AS VARCHAR) AS cancellation_policy_type,
    CAST(lead_time_days AS INTEGER) AS lead_time_days,
    CAST(customer_rating_score AS INTEGER) AS customer_rating_score,
    CAST(local_search_demand_score AS INTEGER) AS local_search_demand_score
FROM read_csv_auto('02_raw_data/terrazas_bookings_staging.csv');

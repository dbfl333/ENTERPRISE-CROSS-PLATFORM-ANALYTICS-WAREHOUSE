-- Clean and structure Tenant D: Terrazas-home (Venue Administration Platform)
-- Inputs: terrazas_raw_bookings.csv, juarez_weather_forecast_raw.csv, mexico_holidays_raw.csv, osm_venue_density_raw.csv

CREATE OR REPLACE TABLE staging_terrazas_bookings AS
WITH Bookings AS (
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
    FROM read_csv_auto('02_raw_data/terrazas_raw_bookings.csv')
),
Weather AS (
    SELECT
        TRY_CAST(forecast_date AS DATE) AS w_date,
        CAST(max_temp AS DOUBLE) AS max_temp,
        CAST(precipitation AS DOUBLE) AS precipitation
    FROM read_csv_auto('02_raw_data/juarez_weather_forecast_raw.csv')
),
Holidays AS (
    SELECT
        TRY_CAST(date AS DATE) AS h_date,
        CAST(name AS VARCHAR) AS holiday_name
    FROM read_csv_auto('02_raw_data/mexico_holidays_raw.csv')
),
Density AS (
    SELECT
        CAST(post_code AS VARCHAR) AS post_code,
        CAST(place_name AS VARCHAR) AS place_name,
        CAST(state AS VARCHAR) AS state
    FROM read_csv_auto('02_raw_data/osm_venue_density_raw.csv')
    LIMIT 1
)
SELECT
    b.reservation_id,
    b.venue_id,
    b.customer_id,
    b.event_type,
    b.check_in_timestamp,
    b.check_out_timestamp,
    b.total_hours_booked,
    b.base_venue_price,
    b.seasonal_multiplier,
    b.inventory_rentals_json,
    b.service_addons_json,
    b.security_deposit_held,
    b.cleaning_fee,
    b.total_gross_amount,
    b.payment_status,
    b.contract_signed_status,
    b.cancellation_policy_type,
    b.lead_time_days,
    b.customer_rating_score,
    b.local_search_demand_score,
    COALESCE(w.max_temp, 35.0) AS forecast_max_temp,
    COALESCE(w.precipitation, 0.0) AS forecast_precipitation,
    COALESCE(h.holiday_name, 'None') AS holiday_name,
    COALESCE(d.post_code, '32000') AS zip_code,
    COALESCE(d.place_name, 'Centro') AS neighborhood,
    COALESCE(d.state, 'Chihuahua') AS location_state
FROM Bookings b
LEFT JOIN Weather w ON CAST(b.check_in_timestamp AS DATE) = w.w_date
LEFT JOIN Holidays h ON CAST(b.check_in_timestamp AS DATE) = h.h_date
CROSS JOIN Density d;

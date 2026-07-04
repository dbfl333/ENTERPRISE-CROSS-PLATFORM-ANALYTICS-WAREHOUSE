-- Clean and structure Tenant B: Agentic Prompt Labs (SaaS & AI Infrastructure Monitoring)
-- Input: 02_raw_data/prompt_raw_telemetry.csv

CREATE OR REPLACE TABLE clean_prompt_telemetry AS
SELECT
    request_id,
    CAST(timestamp AS TIMESTAMP) AS log_timestamp,
    CAST(prompt_token_count AS INTEGER) AS prompt_token_count,
    CAST(completion_token_count AS INTEGER) AS completion_token_count,
    -- Filter out logical anomalies (latencies > 60000ms as outliers/anomalies)
    CAST(latency_ms AS INTEGER) AS latency_ms,
    CASE 
        WHEN CAST(latency_ms AS INTEGER) >= 60000 THEN TRUE 
        ELSE FALSE 
    END AS is_latency_outlier,
    CAST(http_status_code AS INTEGER) AS http_status_code,
    agent_sub_routine,
    -- Parse model and temperature from metadata using regex to handle malformed JSON strings robustly
    COALESCE(
        NULLIF(REGEXP_EXTRACT(meta_json, '"model"\s*:\s*"([^"]+)"', 1), ''), 
        'Unknown'
    ) AS model,
    COALESCE(
        TRY_CAST(REGEXP_EXTRACT(meta_json, '"temperature"\s*:\s*([0-9.]+)', 1) AS DOUBLE),
        0.7
    ) AS temperature
FROM read_csv_auto('02_raw_data/prompt_raw_telemetry.csv')
WHERE CAST(latency_ms AS INTEGER) < 60000; -- Explicit filter out of out-of-bounds anomalies

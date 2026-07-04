# Skill 3: Relational Schema Design & Transformations (ETL)

## Objective
Ingest raw CSV datasets from multiple tenants, clean anomalies using SQL transformations inside DuckDB, and store the unified structured schemas in a single analytical database binary.

## Transforming Rules
1. **Engine Standard:** Execute all database transformations inside **DuckDB**. Do not load full tables into in-memory pandas DataFrames for cleaning; leverage SQL query compilation.
2. **Syntax Syntax:** Use pure PostgreSQL-compatible SQL queries inside DuckDB engine scripts.
3. **Data Cleaning Rules:**
   - **Type Casting:** Use explicit casts, e.g., `CAST(date_column AS TIMESTAMP)`.
   - **Null Handling:** Replace null/missing metrics with deterministic default values using `COALESCE`.
   - **Anomaly Filtering:** Clean out logical impossibilities, e.g., filtering out infinite latency runs (e.g. `WHERE latency_ms < 60000`).
   - **Price Normalization:** Parse mixed currency and number strings to standard numeric values.
4. **Relational Modeling:**
   - Design a **Star Schema** model.
   - Separate dimensions (e.g. `dim_users`, `dim_assets`, `dim_dates`) and facts (e.g. `fact_transactions`, `fact_telemetry`, `fact_bookings`).
   - Write final output to `04_clean_data/analytics_production.duckdb`.

# Skill 2: Data Synthesis Engine Paradigms

## Objective
Programmatically generate realistic, multi-tenant "messy" datasets (AI Markets Shop, Agentic Prompt Labs, Terrazas-home) that mimic raw production inputs with logical, formatting, and structural anomalies.

## Constraints & Requirements
1. **Faker Integration:** Use the Python `Faker` library alongside built-in standard file and CSV tools to output raw data files to the `02_raw_data/` folder.
2. **Chaos Variables Injection:**
   - **Tenant A (AI Markets Shop):** Funnel steps: `Session Start -> Item Viewed -> Added to Cart -> Cart Abandoned vs. Checkout Success`. Inject null user IDs for abandoned paths, empty customer geographic fields, and inconsistent pricing formats (`$150.00`, `150`, `150,00 USD`).
   - **Tenant B (Agentic Prompt Labs):** 100k API logs tracking latency and tokens. Inject latencies exceeding 30,000ms, malformed/incomplete JSON strings, and HTTP 429 status code clusters.
   - **Tenant C (Terrazas-home):** Calendar reservations. Inject mixed timestamp structures (ISO-8601 mixed with plain text like "July 3rd, 2026"), double-booking scheduling overlaps, and zero-dollar pricing discrepancies.
3. **Relational Anomalies:** Maintain mathematical links but introduce structural anomalies. For example, ensure a percentage of Tenant A sessions point to non-existent user IDs to test external key integrity.

## Generation Execution Plan
- Write `01_data_generation/generate_shop_metrics.py`
- Write `01_data_generation/generate_prompt_telemetry.py`
- Write `01_data_generation/generate_terrazas_bookings.py`
- Execute each script to output CSVs directly to `02_raw_data/`.

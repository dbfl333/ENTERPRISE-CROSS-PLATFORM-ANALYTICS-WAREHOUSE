# MASTER ARCHITECTURE BLUEPRINT: ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE

## 1. PROJECT PARAMETERS & SECURITY PROTOCOLS
- **Core Technology Stack:** Python, DuckDB (PostgreSQL syntax engine), Streamlit.
- **Local Isolation Rules:** 
  - Zero external cloud execution network requests allowed during transformations.
  - Ingestion processes operate strictly via explicit local flat files or verified target API endpoints.
- **Data Governance & Exclusions:**
  - Mandatory programmatic blocking of localized environment metadata logs (`.env`) inside the root repository tracking.
  - Strict classification of compiled analytical storage binaries (`*.duckdb`, `*.db`) as local-only components.

---

## 2. SYSTEM CODEBASE ARCHITECTURE
```text
ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE/
├── .agents/                          # System Agent Instructions
│   └── skills/                       # Granular technical capabilities
│       └── DATA_ENGINEERING_PROTOCOLS.md
├── 01_api_ingestion/                 # Primary programmatic extraction scripts
│   ├── shopify_extractor.py          # Real-time Shopify API execution
│   └── binance_extractor.py          # Real-time Binance API execution
├── 02_raw_data/                      # Disconnected data landing arrays (Dirty Layer)
│   ├── shop_raw_orders.csv           # Raw Shopify order payloads
│   ├── binance_btc_raw.csv           # Raw historical market metrics
│   ├── prompt_telemetry_staging.csv  # Placeholder ingestion stream
│   └── terrazas_bookings_staging.csv # Placeholder ingestion stream
├── 03_etl_pipelines/                 # Pure SQL/DuckDB transformation scripts
│   ├── clean_shop_data.sql           # Shopify parsing and normalization
│   ├── clean_binance_data.sql        # Market data standardization
│   └── merge_unified_warehouse.sql   # Star schema multi-tenant integration
├── 04_clean_data/                    # Production relational storage layer
│   └── analytics_production.duckdb  # Central database binary
├── 05_dashboard/                     # Streamlit enterprise dashboard engine
│   ├── app.py                        # Interface execution core
│   └── pages/                        # Multi-tenant deep-dive tracking modules
│       ├── 01_executive_overview.py
│       ├── 02_shop_analytics.py
│       ├── 03_gtrend_analytics.py
│       ├── 04_prompt_labs_staging.py
│       └── 05_terrazas_staging.py
└── requirements.txt                  # Local deployment environment specification
```

---

## 3. GRANULAR MULTI-TENANT SPECIFICATIONS

### Tenant A: AI Markets Shop (E-Commerce Ingestion)

* **Data Source:** Live Shopify REST Admin API.
* **Authentication:** Requires `SHOPIFY_ACCESS_TOKEN` read securely from the local `.env` file.
* **Ingestion Rule:** Query and extract all historical order entries back to store creation.
* **Target Fields:** `order_id`, `total_price`, `currency`, `created_at`, `customer.id`, `financial_status`.

### Tenant B: G-Trend Screener (Quantitative Market Analysis)

* **Data Source:** Public Binance API (`/api/v3/klines`).
* **Authentication:** Public endpoints (Zero token required).
* **Ingestion Rule:** Pass a historical limit parameter of `500` daily candlestick rows to backfill more than a year of continuous data.
* **Target Fields:** `open_time`, `open`, `high`, `low`, `close`, `volume`, `number_of_trades`.

### Tenant C: Agentic Prompt Labs & Tenant D: Terrazas-home (Empty Staging Layers)

* **Status:** Pre-launch. Zero fake data generation allowed.
* **Engineering Requirement:** Build and provision empty target schemas inside DuckDB to establish complete pipeline readiness for live tracking streams.

---

## 4. TERMINAL ENVIROMENT PROVISIONING (GIT BASH)

All terminal deployments on Windows host hardware must execute via Git Bash utilizing standard Linux CLI inputs:

```bash
# Initialize repository tracking
git init

# Establish environment blocks before first staging commit
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.duckdb" >> .gitignore
echo "*.csv" >> .gitignore

# Set up clean execution environment
python -m venv venv
source venv/Scripts/activate
pip install duckdb pandas streamlit requests
pip freeze > requirements.txt
```

---

## 5. REUSABLE INGESTION & TRANSFORMATION BLUEPRINTS

### Python API Extraction Pattern

```python
import os
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def run_shopify_extraction():
    token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    endpoint = "https://ai-markets.myshopify.com/admin/api/2024-01/orders.json?status=any"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json().get('orders', [])
        df = pd.json_normalize(data)
        df.to_csv("02_raw_data/shop_raw_orders.csv", index=False)
        logging.info("Shopify extraction complete.")
```

### DuckDB SQL Processing Standards (PostgreSQL Syntax)

```sql
-- Explicit Type Casting, Cleaning, and Null Handling via CTEs
CREATE TABLE IF NOT EXISTS staging_prompt_telemetry (
    request_id VARCHAR PRIMARY KEY,
    agent_id VARCHAR,
    prompt_tokens INT,
    latency_ms INT,
    execution_timestamp TIMESTAMP
);

WITH ProcessedOrders AS (
    SELECT 
        CAST(id AS VARCHAR) AS order_identity,
        COALESCE(LOWER(TRIM(email)), 'offline_checkout@domain.com') AS standardized_email,
        CAST(REPLACE(CAST(total_price AS VARCHAR), '$', '') AS DECIMAL(10,2)) AS net_revenue,
        CAST(created_at AS TIMESTAMP) AS conversion_timestamp,
        ROW_NUMBER() OVER(PARTITION BY id ORDER BY created_at DESC) as row_num
    FROM read_csv_auto('02_raw_data/shop_raw_orders.csv')
)
SELECT * FROM ProcessedOrders WHERE row_num = 1;
```

---

## 6. STREAMLIT PERFORMANCE INTEGRATION

```python
import streamlit as st
import duckdb

@st.cache_data
def load_warehouse_data(query_string):
    conn = duckdb.connect('../04_clean_data/analytics_production.duckdb', read_only=True)
    dataframe = conn.execute(query_string).df()
    conn.close()
    return dataframe

st.title("Enterprise Cross-Platform Warehouse")
st.dataframe(load_warehouse_data("SELECT * FROM staging_prompt_telemetry"))
```

---

## 7. AUTOMATED CROSS-REPOSITORY DOCUMENTATION MANDATE

You are required to access the adjacent local repositories: `AI Markets Shop`, `Agentic Prompt Labs`, `Terrazas-home`, and `G-Trend`. Inspect their structures and generate a comprehensive `README.md` for each using this standardized engineering blueprint:

1. **System Objective:** Clear technical explanation of what the application does.
2. **Architecture Stack:** Exact summary of languages, frameworks, and deployment components.
3. **Data Logging Profile:** Document every schema field the app generates.
4. **Data Warehouse Ingestion Link:** Explicitly append the integration path: *"All active telemetry and system logging streams produced by this codebase are directly piped into the centralized ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE engine."*

# 🏭 Enterprise Cross-Platform Analytics Warehouse

> **Live App:** [enterprise-cross-platform-analytics-warehouse.streamlit.app](https://enterprise-cross-platform-analytics-warehouse.streamlit.app/)
> **GitHub:** [dbfl333/ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE](https://github.com/dbfl333/ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE)

A production-grade, multi-tenant data engineering platform that ingests live data from **Shopify, Binance, Google Trends, GitHub, HackerNews, arXiv, Open-Meteo, Blockchain.info, CoinGecko, Alternative.me, Frankfurter, GeoJS, Wikipedia, OpenStreetMap, and Terrazas venue systems** — transforms everything through **DuckDB ETL pipelines** governed by a **WrenAI Semantic Layer** — and surfaces all insights through a **Streamlit enterprise analytics dashboard** deployed on **Streamlit Cloud**.

---

## 🗂️ Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack & Architecture](#-tech-stack--architecture)
- [Multi-Tenant Data Model](#-multi-tenant-data-model)
- [Core Features](#-core-features)
- [Project Structure](#-project-structure)
- [API Data Sources](#-api-data-sources)
- [ETL Pipeline](#-etl-pipeline)
- [WrenAI Semantic Layer](#-wrenai-semantic-layer)
- [Streamlit Dashboard Pages](#-streamlit-dashboard-pages)
- [Setup & Local Development](#-setup--local-development)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [CI/CD Automation](#-cicd-automation)
- [Data Governance](#-data-governance)

---

## 🎯 Project Overview

The **Enterprise Cross-Platform Analytics Warehouse** is a **data engineering portfolio project** built to demonstrate end-to-end data architecture across four distinct business domains (tenants):

| Tenant | Domain | Primary Data Source |
|--------|--------|---------------------|
| **A — AI Markets Shop** | E-Commerce Analytics | Shopify Admin REST API |
| **B — G-Trend Screener** | Crypto & Market Intelligence | Binance API, CoinGecko, Alternative.me |
| **C — Agentic Prompt Labs** | AI Tooling Demand Telemetry | GitHub API, HackerNews, arXiv |
| **D — Terrazas Venue** | Hospitality & Event Management | Terrazas booking system, Open-Meteo, OSM |

All four tenants funnel data through a **shared DuckDB warehouse** governed by the **WrenAI Semantic Layer**, ensuring every dashboard query is validated, qualified, and dry-planned before execution. The final output is a **multi-page Streamlit analytics suite** accessible live at the URL above.

---

## 🛠️ Tech Stack & Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               LIVE API SOURCES (16 integrations)            │
│  Shopify · Binance · Frankfurter · GeoJS · Wikipedia        │
│  CoinGecko · Alternative.me · Blockchain.info · PyTrends    │
│  GitHub API · HackerNews · arXiv · Open-Meteo               │
│  Mexico Holidays · OpenStreetMap · Terrazas Bookings         │
└──────────────────────────┬──────────────────────────────────┘
                           │ Python extraction scripts
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              02_raw_data/  (CSV Landing Zone)                │
│  20+ raw CSV files — dirty, untyped, unaggregated           │
└──────────────────────────┬──────────────────────────────────┘
                           │ DuckDB SQL transformations
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         03_etl_pipelines/  (DuckDB SQL Engine)               │
│  Type casting · NULL handling · deduplication · star schema  │
└──────────────────────────┬──────────────────────────────────┘
                           │ analytics_production.duckdb
                           ▼
┌─────────────────────────────────────────────────────────────┐
│      wren_project/  (WrenAI Semantic Layer — MDL)            │
│  Governed SQL routing · AST dry-plan · model definitions     │
└──────────────────────────┬──────────────────────────────────┘
                           │ WrenEngine Python SDK
                           ▼
┌─────────────────────────────────────────────────────────────┐
│      05_dashboard/  (Streamlit 1.30+ Cloud Deployment)       │
│  Multi-page app · Altair charts · live sync · semantic UI    │
└─────────────────────────────────────────────────────────────┘
```

**Languages:** Python 3.11+, SQL (DuckDB/PostgreSQL syntax), YAML, JSON

**Core Libraries:**
| Library | Role |
|---------|------|
| `duckdb >= 1.0.0` | In-process analytical SQL engine — the warehouse core |
| `streamlit >= 1.30.0` | Multi-page analytics dashboard framework |
| `pandas >= 2.0.0` | DataFrame I/O and tabular transformation |
| `pyarrow >= 14.0.0` | Columnar memory format for DuckDB data interchange |
| `pytrends >= 4.9.0` | Google Trends unofficial API client |
| `altair >= 5.0.0` | Declarative Vega-Lite charting for Streamlit |
| `faker >= 22.0.0` | Realistic synthetic data generation for fallback mode |
| `requests >= 2.31.0` | HTTP client for all REST API integrations |
| `python-dotenv >= 1.0.0` | Secure `.env` loading for local credential management |
| `wren` | WrenAI Python SDK — semantic layer query governance |

---

## 📦 Multi-Tenant Data Model

### Tenant A — AI Markets Shop

**Core Tables:**
- `fact_shop_orders` — Complete Shopify checkout funnel with 19 fields: `checkout_id`, `customer_id`, `customer_locale`, `referring_site`, `landing_site`, `abandoned_checkout_url`, `created_at`, `completed_at`, `time_in_funnel_seconds`, `currency`, `subtotal_price`, `total_discounts`, `total_tax`, `total_price`, `financial_status`, `cart_token`, `device_type`, `browser_ip`, `buyer_accepts_marketing`, `cancel_reason`
- `staging_ga4_sessions` — Google Analytics 4 session metrics
- `staging_shopify_marketing` — Marketing event attribution
- `ext_shop_forex` — Live USD→MXN/EUR/GBP rates (Frankfurter)
- `ext_shop_buyer_geo` — Buyer IP geolocation (GeoJS)
- `ext_shop_wikipedia` — "Algorithmic trading" Wikipedia pageview trends
- `ext_shop_google_trends` — Google Trends interest for shop-related keywords

### Tenant B — G-Trend Screener

**Core Tables:**
- `fact_binance_klines` — Binance 24hr ticker metrics for BTC, ETH, SOL: `symbol`, `price_change`, `price_change_percent`, `weighted_avg_price`, `last_price`, `open_price`, `high_price`, `low_price`, `volume`, `quote_volume`, `open_time`, `close_time`, `count`
- `ext_binance_btc` — CoinGecko trending narratives with `market_cap_rank`, `price_btc`, `score`
- `ext_crypto_sentiment` — Alternative.me Fear & Greed Index (30-day rolling)
- `ext_blockchain_network` — Blockchain.info Bitcoin network stats: `market_price_usd`, `hash_rate`, `total_fees_btc`, `n_btc_mined`, `minutes_between_blocks`
- `ext_gtrend_google_trends` — Google Trends signals for crypto keywords

### Tenant C — Agentic Prompt Labs

**Core Tables:**
- `staging_prompt_telemetry` — AI agent prompt telemetry with latency and token metrics
- `ext_github_agent_demand` — GitHub repos ranked by `stargazers_count` for AI/agent tooling demand
- `ext_hackernews_tech` — Latest HackerNews story aggregations for tech sentiment
- `ext_arxiv_trends` — arXiv academic paper trends for LLM and agent research
- `ext_prompt_google_trends` — Google Trends data for prompt engineering keywords

### Tenant D — Terrazas Venue Administration

**Core Tables:**
- `staging_terrazas_bookings` — Venue booking records with `total_gross_amount` and capacity metrics
- `ext_juarez_weather` — Open-Meteo weather forecast for Ciudad Juárez (`forecast_date`, `max_temp`)
- `ext_mexico_holidays` — Mexican public holiday calendar for event scheduling
- `ext_osm_venue_density` — OpenStreetMap venue density scores in the local area
- `ext_terrazas_google_trends` — Google Trends interest in venue/event keywords locally

---

## ✨ Core Features

### Data Ingestion
- 🔌 **Live Shopify REST Admin API** extraction with full historical order backfill (2+ years)
- 📈 **Binance Public API** — real-time 24hr tickers for BTC, ETH, SOL with zero auth required
- 🌍 **CoinGecko Trending** — top 7 trending crypto narratives with market cap rank
- 😱 **Alternative.me Fear & Greed Index** — 30-day rolling sentiment series
- ⛓️ **Blockchain.info Network Stats** — live hash rate, mining fees, block time
- 💱 **Frankfurter Forex API** — live USD/MXN/EUR/GBP rates
- 📍 **GeoJS Geolocation** — buyer IP-to-country mapping
- 📖 **Wikipedia Pageviews API** — article view trends as demand proxy
- 🔥 **Google Trends (PyTrends)** — multi-keyword search interest across all 4 tenants
- ⭐ **GitHub API** — AI agent repo stargazer demand metrics
- 📰 **HackerNews API** — trending tech story aggregation
- 🎓 **arXiv API** — AI/LLM academic paper trend extraction
- 🌤️ **Open-Meteo API** — 7-day weather forecast for venue event planning
- 🗺️ **OpenStreetMap Overpass API** — venue density spatial queries
- 🗓️ **Mexican Public Holidays** — calendar enrichment for Terrazas booking analytics
- 📊 **GA4 Session Data** — Google Analytics 4 web session attribution
- **Intelligent fallback generators** — all extractors include Faker-powered mock data so the pipeline never stops

### ETL & Transformation
- 🦆 **DuckDB as the warehouse engine** — PostgreSQL-syntax SQL in-process, zero server required
- 🧹 **Explicit type casting** with `CAST`, `COALESCE`, `TRIM` across all staging tables
- 🔑 **ROW_NUMBER() deduplication** on all fact tables
- ⭐ **Star schema design** — fact tables joined to dimension and external tables
- 📂 **`read_csv_auto()`** — schema-inferred CSV ingestion for all 20+ raw files
- 🔄 **`run_etl.py`** — single-command ETL orchestrator that calls all extractors then runs SQL pipelines

### WrenAI Semantic Layer
- 🧠 **MDL (Modeling Definition Language)** — YAML-defined semantic models auto-scaffolded from DuckDB schema
- ✅ **AST dry-plan** — every SQL query is compiled and inspected before execution
- 🔒 **Governed query routing** — all dashboard SQL passes through `WrenEngine.query()` for validation
- 🎛️ **Interactive Semantic Playground** — run any of 4 predefined queries with live AST viewer in the dashboard
- 📋 **`wren_project/target/mdl.json`** — compiled manifest loaded at runtime via Base64 encoding

### Streamlit Dashboard
- 🏠 **Executive Overview** — 4 KPI tiles, revenue timeline, BTC price area chart, semantic playground
- 🛍️ **AI Markets Shop** (`02_AI_MARKETS_SHOP.py`) — Shopify funnel analytics, device type breakdown, marketing attribution
- 🔍 **Markets Ad Insights** (`03_AI_MARKETS_AD_INSIGHTS.py`) — advertising performance deep-dive
- 📡 **G-Trend Screener** (`04_GTREND_SCREENER.py`) — crypto market data with Fear & Greed, blockchain stats
- 💡 **G-Trend Ad Insights** (`05_GTREND_AD_INSIGHTS.py`) — trend-based advertising signal panel
- 🤖 **Agentic Prompt Labs** (`06_AGENTIC_PROMPT_LABS.py`) — AI demand telemetry, GitHub stars, HackerNews, arXiv trends
- 🧬 **Prompt Labs Ad Insights** (`07_PROMPT_LABS_AD_INSIGHTS.py`) — prompt engineering market signals
- 🏨 **Terrazas Administration** (`08_TERRAZAS_ADMINISTRATION.py`) — venue booking analytics, weather forecast, holiday calendar
- 📊 **Terrazas Ad Insights** (`09_TERRAZAS_AD_INSIGHTS.py`) — venue marketing and event demand insights
- 🔄 **Live Sync Button** — clears all Streamlit cache resources on demand
- 📅 **Real-time timestamp** on every page showing last data refresh

### Infrastructure & Automation
- ⚙️ **GitHub Actions CI/CD** (`.github/workflows/daily_etl.yml`) — nightly automated ETL run
- 🐳 **Dev Container** (`.devcontainer/`) — reproducible Python development environment
- 🔐 **`.gitignore` governed** — `.env`, `*.duckdb`, `*.db`, `__pycache__`, `.agents/` all excluded
- 🤖 **Agent-ready architecture** — `.agents/` skill folder with `DATA_ENGINEERING_PROTOCOLS.md`

---

## 📁 Project Structure

```
ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE/
│
├── 01_api_ingestion/                      # Live API extraction layer
│   ├── shopify_extractor.py               # Shopify Admin API + 4 external enrichment sources
│   ├── binance_extractor.py               # Binance, CoinGecko, Alternative.me, Blockchain.info
│   ├── ga4_extractor.py                   # Google Analytics 4 session data
│   ├── market_demand_extractor.py         # GitHub, HackerNews, arXiv, Open-Meteo
│   ├── shopify_marketing_extractor.py     # Shopify marketing event attribution
│   └── terrazas_extractor.py             # Terrazas bookings, weather, holidays, OSM
│
├── 02_raw_data/                           # CSV landing zone (20+ files, gitignored)
│   ├── shop_raw_orders.csv
│   ├── ga4_sessions.csv
│   ├── shopify_marketing_events.csv
│   ├── shop_forex_rates_raw.csv
│   ├── shop_buyer_geo_raw.csv
│   ├── shop_wikipedia_trends_raw.csv
│   ├── google_trends_shop.csv
│   ├── binance_metrics.csv
│   ├── binance_btc_raw.csv
│   ├── crypto_sentiment_raw.csv
│   ├── blockchain_network_raw.csv
│   ├── google_trends_gtrend.csv
│   ├── prompt_raw_telemetry.csv
│   ├── github_agent_demand_raw.csv
│   ├── hackernews_tech_raw.csv
│   ├── arxiv_academic_trends_raw.csv
│   ├── google_trends_prompt.csv
│   ├── terrazas_raw_bookings.csv
│   ├── juarez_weather_forecast_raw.csv
│   ├── mexico_holidays_raw.csv
│   ├── osm_venue_density_raw.csv
│   └── google_trends_terrazas.csv
│
├── 03_etl_pipelines/                      # DuckDB SQL transformation layer
│   ├── merge_unified_warehouse.sql        # Master 4-tenant CREATE OR REPLACE TABLE script
│   ├── clean_shop_data.sql                # Shopify type casting, dedup, star schema build
│   ├── clean_binance_data.sql             # Market data standardization, OHLCV normalization
│   └── staging_terrazas_schema.sql        # Terrazas empty schema provisioning
│
├── 04_clean_data/                         # Production DuckDB warehouse (gitignored)
│   └── analytics_production.duckdb        # Central OLAP database binary
│
├── 05_dashboard/                          # Streamlit analytics dashboard
│   ├── app.py                             # Entry point: Executive Overview + WrenAI playground
│   └── pages/
│       ├── 02_AI_MARKETS_SHOP.py
│       ├── 03_AI_MARKETS_AD_INSIGHTS.py
│       ├── 04_GTREND_SCREENER.py
│       ├── 05_GTREND_AD_INSIGHTS.py
│       ├── 06_AGENTIC_PROMPT_LABS.py
│       ├── 07_PROMPT_LABS_AD_INSIGHTS.py
│       ├── 08_TERRAZAS_ADMINISTRATION.py
│       └── 09_TERRAZAS_AD_INSIGHTS.py
│
├── wren_project/                          # WrenAI Semantic Layer
│   ├── wren_project.yml                   # Project configuration
│   ├── relationships.yml                  # Cross-tenant table relationships
│   ├── models/                            # MDL model YAML definitions
│   ├── views/                             # Wren view definitions
│   ├── cubes/                             # Wren cube aggregations
│   ├── knowledge/                         # Business knowledge definitions
│   ├── apps/my_bi_app/                    # GenBI WebAssembly app (wren-core-wasm)
│   └── target/mdl.json                    # Compiled manifest — loaded at runtime
│
├── .github/workflows/
│   └── daily_etl.yml                      # Nightly GitHub Actions ETL automation
│
├── .devcontainer/                         # VS Code Dev Container configuration
├── core_system_framework.md               # Master architecture blueprint document
├── run_etl.py                             # Single-command ETL orchestrator
├── requirements.txt                       # Python dependency manifest
├── .gitignore                             # Governance: excludes .env, *.duckdb, agents/
└── README.md                              # This document
```

---

## 🔌 API Data Sources

| # | Source | Endpoint | Tenant | Auth |
|---|--------|----------|--------|------|
| 1 | Shopify Admin REST | `/{store}/admin/api/2024-04/orders.json` | A | `SHOPIFY_ACCESS_TOKEN` |
| 2 | Frankfurter Forex | `api.frankfurter.app/latest` | A | None |
| 3 | GeoJS Geolocation | `get.geojs.io/v1/ip/geo.json` | A | None |
| 4 | Wikipedia Pageviews | `wikimedia.org/api/rest_v1/metrics/pageviews/...` | A | None |
| 5 | Binance 24hr Ticker | `api.binance.com/api/v3/ticker/24hr` | B | None |
| 6 | CoinGecko Trending | `api.coingecko.com/api/v3/search/trending` | B | None |
| 7 | Alternative.me F&G | `api.alternative.me/fng/?limit=30` | B | None |
| 8 | Blockchain.info Stats | `api.blockchain.info/stats` | B | None |
| 9 | PyTrends (Google Trends) | Unofficial API (4 tenants) | A/B/C/D | None |
| 10 | GitHub API | `api.github.com/search/repositories` | C | None |
| 11 | HackerNews API | `hacker-news.firebaseio.com/v0/...` | C | None |
| 12 | arXiv API | `export.arxiv.org/api/query` | C | None |
| 13 | Open-Meteo | `api.open-meteo.com/v1/forecast` | D | None |
| 14 | OpenStreetMap Overpass | `overpass-api.de/api/interpreter` | D | None |
| 15 | Mexico Holidays | `date.nager.at/api/v3/PublicHolidays/MX/...` | D | None |
| 16 | GA4 Data API | `analyticsdata.googleapis.com/v1beta/...` | A | Service Account |

---

## 🔄 ETL Pipeline

The ETL pipeline runs in three sequential stages:

### Stage 1: API Extraction (`01_api_ingestion/`)
Each extractor script connects to its target API, falls back to a realistic Faker-powered mock generator if the API is unavailable, and writes output to `02_raw_data/*.csv`.

### Stage 2: DuckDB Transformation (`03_etl_pipelines/`)
```sql
-- Example: Shopify fact table creation with governed schema
CREATE OR REPLACE TABLE fact_shop_orders AS
SELECT * FROM read_csv_auto('02_raw_data/shop_raw_orders.csv');

-- With CTEs for deduplication
WITH ProcessedOrders AS (
    SELECT *,
        ROW_NUMBER() OVER(PARTITION BY checkout_id ORDER BY created_at DESC) as row_num
    FROM read_csv_auto('02_raw_data/shop_raw_orders.csv')
)
SELECT * EXCLUDE(row_num) FROM ProcessedOrders WHERE row_num = 1;
```

### Stage 3: Warehouse Compilation
The `run_etl.py` orchestrator:
1. Calls all 6 extractors in sequence
2. Opens a DuckDB connection to `04_clean_data/analytics_production.duckdb`
3. Executes `merge_unified_warehouse.sql` to register all 22 tables
4. Closes the connection — warehouse is ready for Streamlit

**To run the full ETL pipeline:**
```bash
python run_etl.py
```

---

## 🧠 WrenAI Semantic Layer

The WrenAI semantic layer adds a **governance and translation layer** between the raw DuckDB warehouse and the Streamlit dashboard:

1. **MDL Schema** — defined in `wren_project/models/*.yml`, maps physical table columns to semantic business terms
2. **Manifest Compilation** — `wren_project/target/mdl.json` is the compiled artifact loaded at runtime
3. **WrenEngine** — the Python SDK instantiates the engine with the manifest + DuckDB connection info
4. **Query Governance** — every SQL query is routed through `engine.query()` ensuring it is validated against the semantic model
5. **AST Dry Plan** — `engine.dry_plan(sql)` returns the compiled query execution plan, visible in the Executive Overview playground

```python
# Runtime engine initialization in app.py
engine = wren.WrenEngine(
    manifest_str=manifest_b64,
    data_source="duckdb",
    connection_info={"url": "path/to/04_clean_data", "format": "duckdb"}
)

# Governed query execution
result_df = engine.query("SELECT * FROM fact_shop_orders").to_pandas()
ast_plan  = engine.dry_plan("SELECT * FROM fact_shop_orders")
```

---

## 🖥️ Streamlit Dashboard Pages

| Page | File | Key Metrics |
|------|------|-------------|
| Executive Overview | `app.py` | Shop Revenue, BTC Price, Prompt Requests, Terrazas Revenue |
| AI Markets Shop | `02_AI_MARKETS_SHOP.py` | Funnel completion, device breakdown, abandonment analysis |
| Markets Ad Insights | `03_AI_MARKETS_AD_INSIGHTS.py` | Marketing attribution, referring site ranking |
| G-Trend Screener | `04_GTREND_SCREENER.py` | BTC/ETH/SOL ticker, Fear & Greed, blockchain network stats |
| G-Trend Ad Insights | `05_GTREND_AD_INSIGHTS.py` | Crypto trend signals, trading volume correlations |
| Agentic Prompt Labs | `06_AGENTIC_PROMPT_LABS.py` | GitHub stars, HackerNews stories, arXiv paper trends |
| Prompt Labs Insights | `07_PROMPT_LABS_AD_INSIGHTS.py` | AI demand scoring, latency benchmarks |
| Terrazas Admin | `08_TERRAZAS_ADMINISTRATION.py` | Booking volumes, revenue, weather forecast, holidays |
| Terrazas Ad Insights | `09_TERRAZAS_AD_INSIGHTS.py` | Event demand signals, venue density, local trends |

---

## ⚙️ Setup & Local Development

### Prerequisites
- Python 3.11+
- Git
- A `.env` file with required credentials (see below)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dbfl333/ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE.git
cd ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Create your .env file
cp .env.example .env   # then fill in your credentials

# 5. Run the ETL pipeline to populate the warehouse
python run_etl.py

# 6. Launch the Streamlit dashboard
streamlit run 05_dashboard/app.py
```

The app will open at `http://localhost:8501`.

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Tenant A — AI Markets Shop
SHOPIFY_ACCESS_TOKEN=your_shopify_admin_api_token
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com

# Tenant A — Google Analytics 4 (optional — requires google-analytics-data package)
GA4_PROPERTY_ID=your_ga4_property_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json

# Optional: Used only if extending to authenticated external APIs
BINANCE_API_KEY=optional_binance_api_key
BINANCE_API_SECRET=optional_binance_api_secret
```

> **Note:** If `SHOPIFY_ACCESS_TOKEN` is not set, the Shopify extractor automatically generates 200 realistic synthetic orders using the Faker library. All other API endpoints are public and require no credentials.

---

## 🚀 Deployment

This app is deployed on **Streamlit Community Cloud**.

**Live URL:** [enterprise-cross-platform-analytics-warehouse.streamlit.app](https://enterprise-cross-platform-analytics-warehouse.streamlit.app/)

### Streamlit Cloud Configuration
- **Entry point:** `05_dashboard/app.py`
- **Branch:** `main`
- **Python version:** 3.11
- **Secrets:** Set `SHOPIFY_ACCESS_TOKEN` and other credentials in the Streamlit Cloud Secrets manager (equivalent to `.env` in production)

### Deploying Your Own Instance
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your fork → branch `main` → main file `05_dashboard/app.py`
5. Add your secrets in the Streamlit Cloud dashboard
6. Click **Deploy**

---

## ⚡ CI/CD Automation

A **GitHub Actions workflow** (`.github/workflows/daily_etl.yml`) runs nightly to:
1. Check out the repository
2. Set up the Python environment
3. Run `python run_etl.py` to refresh all 16 data sources
4. Commit and push updated raw data CSVs back to the repository
5. Trigger a Streamlit Cloud redeploy

This ensures the live dashboard always displays fresh data without any manual intervention.

---

## 🔒 Data Governance

| Rule | Implementation |
|------|----------------|
| No secrets in git | `.env` in `.gitignore` |
| No warehouse binaries in git | `*.duckdb`, `*.db` in `.gitignore` |
| No agent instructions exposed | `.agents/`, `agents/` in `.gitignore` (public repo) |
| No raw cache in git | `__pycache__/`, `*.pyc` in `.gitignore` |
| Semantic query governance | All SQL routed through WrenAI Engine |
| Fallback safety net | Every extractor has a Faker mock fallback |

---

## 📄 License

This project is open source and available for portfolio and educational demonstration purposes.

---

*Built with 🦆 DuckDB · 🎈 Streamlit · 🧠 WrenAI · 🐍 Python*
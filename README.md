# ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE

> A centralized, multi-tenant analytical data warehouse integrating live API extraction pipelines, DuckDB star schema transformations, and a Streamlit enterprise BI dashboard — built to track, analyze, and unify business intelligence across four separate commercial platforms.

---

## 🏗️ System Architecture

```text
ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE/
├── .agents/                          # Agent protocols and skill definitions
│   └── skills/
│       ├── DATA_ENGINEERING_AGENT_PROTOCOLS.md
│       └── PORTFOLIO_README_TEMPLATES.md
├── .github/
│   └── workflows/
│       └── daily_etl.yml             # Nightly GitHub Actions automation
├── 01_api_ingestion/                 # Live API extraction scripts
│   ├── shopify_extractor.py          # Shopify REST Admin API → checkout funnel (20 fields)
│   ├── binance_extractor.py          # Binance Public API → BTC/ETH/SOL klines + indicators
│   ├── market_demand_extractor.py    # Google Trends API → AI keyword demand scoring
│   └── terrazas_extractor.py        # Pre-launch event reservation staging stream
├── 02_raw_data/                      # Dirty data landing zone (gitignored)
│   ├── shop_raw_orders.csv
│   ├── binance_metrics.csv
│   ├── prompt_telemetry_staging.csv
│   └── terrazas_bookings_staging.csv
├── 03_etl_pipelines/                 # DuckDB SQL transformation engine
│   ├── clean_shop_data.sql           # Shopify normalization (TRY_CAST, dedup)
│   ├── clean_binance_data.sql        # Market data standardization
│   ├── staging_terrazas_schema.sql   # Venue staging schema provisioning
│   └── merge_unified_warehouse.sql   # Star schema multi-tenant integration
├── 04_clean_data/                    # Production DuckDB binary (gitignored)
│   └── analytics_production.duckdb
├── 05_dashboard/                     # Streamlit enterprise dashboard
│   ├── app.py                        # Main landing page
│   └── pages/
│       ├── 01_executive_overview.py  # Cross-tenant KPI summary
│       ├── 02_shop_analytics.py      # Shopify funnel analytics
│       ├── 03_gtrend_analytics.py    # Binance screener (BTC/ETH/SOL)
│       ├── 04_prompt_labs_staging.py # Agentic Prompt Labs demand metrics
│       └── 05_terrazas_staging.py    # Terrazas-home venue bookings
├── core_system_framework.md          # Master architecture blueprint
├── run_etl.py                        # Full pipeline orchestrator
└── requirements.txt                  # Python dependency manifest
```

---

## 🏢 Multi-Tenant Business Intelligence Coverage

| Tenant | Application | Data Source | Status |
|--------|-------------|-------------|--------|
| **A** | AI Markets Shop | Shopify REST Admin API | 🟢 Live |
| **B** | G-Trend Screener | Binance Public API | 🟢 Live |
| **C** | Agentic Prompt Labs | Google Trends (pytrends) | 🟢 Live |
| **D** | Terrazas-home | Pre-Launch Telemetry Staging | 🟡 Staging |

---

## 🗃️ Star Schema Design

```
              ┌─────────────┐
              │  dim_dates  │
              │─────────────│
              │ date_key PK │
              │ year        │
              │ month       │
              │ day_of_week │
              └──────┬──────┘
                     │
   ┌─────────────────┼─────────────────┐
   │                 │                 │
┌──┴──────────┐  ┌───┴──────────┐  ┌──┴──────────────┐
│fact_shop_   │  │fact_binance_ │  │  dim_assets      │
│orders       │  │klines        │  │──────────────────│
│─────────────│  │──────────────│  │ asset_id PK      │
│checkout_id  │  │ symbol       │  │ symbol           │
│customer_id  │  │ open_price   │  │ asset_class      │
│total_price  │  │ rsi_14       │  └──────────────────┘
│device_type  │  │ macd_line    │
│funnel_secs  │  │ screener_flag│
└─────────────┘  └─────────────┘
       │
┌──────┴────────┐
│   dim_users   │
│───────────────│
│ customer_id PK│
│ customer_locale│
│ browser_ip    │
└───────────────┘

Staging Tables (pre-launch):
  staging_prompt_telemetry   → Agentic Prompt Labs keyword demand
  staging_terrazas_bookings  → Terrazas-home venue reservations
```

---

## 🚀 Local Setup & Execution

### Prerequisites
- Python 3.12+
- A `.env` file with your API credentials (see below)

### 1. Clone & Install
```bash
git clone https://github.com/dbfl333/ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE.git
cd ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
SHOPIFY_ACCESS_TOKEN=your_shopify_token_here
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
```

### 3. Run the Full ETL Pipeline
```bash
python run_etl.py
```
This will:
1. Execute all 4 API extraction scripts → populate `02_raw_data/`
2. Run all DuckDB SQL transformations → compile `04_clean_data/analytics_production.duckdb`
3. Print a table audit confirming all row counts

### 4. Launch the Dashboard
```bash
streamlit run 05_dashboard/app.py
```
Navigate to `http://localhost:8501` to access the enterprise BI suite.

---

## ⚙️ GitHub Actions — Nightly Automation

The `.github/workflows/daily_etl.yml` workflow runs every night at **midnight UTC** to:
1. Pull the latest data from all 4 API sources
2. Recompile the DuckDB analytical database
3. Commit any updated tracking artifacts

### Required Repository Secrets
Go to: `Settings → Secrets and variables → Actions` and add:

| Secret Name | Value |
|-------------|-------|
| `SHOPIFY_ACCESS_TOKEN` | Your Shopify Admin API token |
| `SHOPIFY_STORE_DOMAIN` | `your-store.myshopify.com` |

---

## 🔒 Data Governance

The following are excluded from Git tracking by `.gitignore`:

| Pattern | Reason |
|---------|--------|
| `.env` | Contains API secrets — never committed |
| `*.duckdb` | Binary database — local-only, rebuilt by pipeline |
| `*.csv` | Raw data landing zone — regenerated each run |
| `02_raw_data/` | Entire dirty data layer excluded |
| `__pycache__/` | Python build artifacts |

---

## 📦 Technology Stack

| Layer | Technology |
|-------|-----------|
| SQL Engine | DuckDB ≥ 1.0 (PostgreSQL syntax) |
| ETL Language | Python 3.12 |
| API Clients | `requests`, `pytrends` |
| Data Processing | `pandas`, `pyarrow` |
| Visualization | Streamlit ≥ 1.30, Altair ≥ 5.0 |
| CI/CD | GitHub Actions |
| Schema Design | Star Schema (Fact + Dimension tables) |

---

## 🔗 Integrated Tenant Repositories

| Repository | Description |
|------------|-------------|
| [AI_MARKETS_SHOP](https://github.com/dbfl333/AI_MARKETS_SHOP) | Shopify e-commerce store for quantitative trading tools |
| [AGENTIC_PROMPT_LABS](https://github.com/dbfl333/AGENTIC_PROMPT_LABS) | Multi-agent LLM orchestration SaaS platform |
| [AI-MARKETS-SHOP-PROMPT-GENERATOR](https://github.com/dbfl333/AI-MARKETS-SHOP-PROMPT-GENERATOR) | React/Vite prompt engineering tool |
| Terrazas-home | Event venue management and reservation engine |

All active telemetry and system logging streams produced by those codebases are directly piped into this centralized ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE engine.
C R I T I C A L   S Y S T E M   R U L E :   W e   a r e   o p e r a t i n g   w i t h i n   a   L I V E   p r o d u c t i o n   b u s i n e s s   a p p l i c a t i o n   t h a t   d i s p l a y s   r e a l   d a t a   f r o m   o u r   d a t a   w a r e h o u s e   t a b l e s .   D O   N O T   u s e   s y n t h e t i c   g e n e r a t o r s   o r   f a k e   d a t a .  
 
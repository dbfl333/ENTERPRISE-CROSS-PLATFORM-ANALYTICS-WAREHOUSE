# MASTER ARCHITECTURE BLUEPRINT: ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE

## 1. STRATEGIC PROJECT INTENT
This repository functions as a centralized Corporate Data Warehouse (CDW) and Business Intelligence (BI) suite. It acts as an operational middleware data layer, unifying disconnected data formats from four independent business systems into a singular, high-performance analytical engine. 

The entire framework operates completely on local architecture, utilizing non-cloud processing nodes to maintain zero external dependency profiles. The codebase is structured to serve as an open public portfolio demonstrating advanced engineering capacity to hiring managers.

---

## 2. ENVIRONMENTAL PARAMETERS & SECURITY PROTOCOLS
- **Core Technology Stack:** Python (Core Engine), DuckDB (Analytical Database Core), Streamlit (Custom Multi-Tenant Presentation Interface Layer).
- **SQL Engine Standard:** Pure PostgreSQL syntax mapping via DuckDB relational database configurations.
- **Local Isolation Rules:** 
  - Zero external cloud execution network requests allowed.
  - Ingestion processes operate strictly against local persistent disk files.
- **Data Governance & Exclusions:**
  - Mandatory programmatic inclusion of localized environment metadata logs (`.env`) inside the root configuration ignore arrays.
  - Strict classification of compiled analytical storage binaries (`*.duckdb`, `*.db`) as excluded local engine storage elements to prevent structural tracking bloat on remote origin branches.

---

## 3. MASTER CODEBASE ARCHITECTURE
```text
ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE/
├── .agents/                          # Direct System Agent Instructions
│   ├── workflows/                    # Multistep operational process execution sheets
│   └── skills/                       # Granular technical capabilities and code paradigms
│       ├── environment_setup.md      # Skill 1: Operating system workspace provisioning
│       ├── generate_messy_data.md    # Skill 2: Data synthesis engine paradigms
│       ├── etl_processing.md         # Skill 3: Relational schema design & transformations
│       ├── dashboard_deployment.md   # Skill 4: Local web app presentation interface
│       └── github_deployment.md      # Skill 5: Public repository creation & deployment
├── 01_data_generation/               # Primary Python programmatic generation scripts
│   ├── generate_shop_metrics.py      # E-commerce user-session funnel transaction generator
│   ├── generate_prompt_telemetry.py  # LLM production metric latency performance generator
│   └── generate_terrazas_bookings.py # Real estate operational reservation matrix generator
├── 02_raw_data/                      # Disconnected data landing arrays (Messy Source Layer)
│   ├── shop_raw_sessions.csv         # Malformed transaction logs
│   ├── prompt_raw_telemetry.csv      # Unstructured API performance latency metrics
│   ├── terrazas_raw_bookings.csv     # Schema-mismatched event reservation sheets
│   └── gtrend_raw_backtests.csv      # True historical quantitative trading engine exports
├── 03_etl_pipelines/                 # Pure SQL/DuckDB algorithmic transformation scripts
│   ├── clean_shop_data.sql           # E-commerce transformation pipeline mapping
│   ├── clean_prompt_data.sql         # API metric latency tracking normalization logic
│   ├── clean_terrazas_data.sql       # Time-series schedule timestamp optimization routing
│   └── merge_unified_warehouse.sql   # Comprehensive cross-tenant analytics integration layout
├── 04_clean_data/                    # Production-ready relational storage layer
│   └── analytics_production.duckdb  # Target deployment relational database binary
├── 05_dashboard/                     # Streamlit enterprise operations visualization node
│   ├── app.py                        # Central dashboard interface execution file
│   └── pages/                        # Multi-tenant deep-dive interface modules
│       ├── 01_executive_overview.py  # Cross-tenant unified strategic dashboard
│       ├── 02_data_quality_etl.py    # Target showcase module displaying messy vs. clean metrics
│       ├── 03_shop_analytics.py      # E-commerce consumer transactional analytics
│       ├── 04_prompt_analytics.py    # System engine API operational performance charts
│       ├── 05_terrazas_analytics.py  # Venue reservation behavior schedules
│       └── 06_gtrend_analytics.py    # Quantitative portfolio risk distribution models
├── core_system_framework.md          # Comprehensive Master Plan Blueprint
└── requirements.txt                  # Local deployment environment specification file
```

---

## 4. GRANULAR TENANT PROFILE & INGESTION PARAMETERS

### Tenant A: AI Markets Shop (E-Commerce Performance Tracking)
* **Operational Context:** Represents consumer transactions and drop-off trends.
* **Temporal Bounds:** Synthesize 4 to 5 months of continuous historical user logs.
* **Target Generation Objective:** 50,000 unique entry records documenting the multi-step transactional conversion funnel (Session Start -> Item Viewed -> Added to Cart -> Cart Abandoned vs. Checkout Success).
* **Injected Chaos Variables:** Null user ID allocations on abandoned paths, empty customer geographic fields, and inconsistent pricing string formatting (e.g., mixing $150.00, 150, and 150,00 USD).

### Tenant B: Agentic Prompt Labs (SaaS & AI Infrastructure Monitoring)
* **Operational Context:** Operational metrics assessing agent performance and framework latency.
* **Temporal Bounds:** Synthesize 12 months of high-velocity logging infrastructure records.
* **Target Generation Objective:** 100,000 unique system interaction entry nodes tracking API call execution footprints.
* **Target Structural Fields:** `request_id`, `prompt_token_count`, `completion_token_count`, `latency_ms`, `http_status_code`, `agent_sub_routine`.
* **Injected Chaos Variables:** Intentionally inject simulated runtime drops: out-of-bounds execution latencies exceeding 30,000ms, incomplete JSON strings, and recurring clusters of HTTP 429 Too Many Requests status codes to replicate real infrastructure bottlenecks.

### Tenant C: Terrazas-home (Event Management & Property Bookings)
* **Operational Context:** Operational schedules, reservation allocations, and event bookings.
* **Temporal Bounds:** Synthesize 4 to 5 months of historical booking activity records.
* **Target Generation Objective:** Complete calendar generation demonstrating seasonal consumer booking distributions.
* **Injected Chaos Variables:** Mixed timestamp standard configurations (combining ISO-8601 strings with localized plain-text strings like July 3rd, 2026), double-booking reservation errors, and zero-dollar reservation discrepancies to test analytical error boundaries.

### Tenant D: G-Trend Screener (Quantitative Strategy Processing)
* **Operational Context:** High-fidelity financial performance models and risk distributions.
* **Data Source Integrity:** NO SYNTHETIC GENERATION. Direct integration of exported performance data tables (CSV format) directly from custom TradingView backtesting frameworks and real-time asset market API data streams.
* **Target Structural Fields:** `trade_id`, `asset_pair`, `entry_timestamp`, `exit_timestamp`, `position_type_long_short`, `profit_loss_percentage`, `max_drawdown_percentage`.
* **Processing Requirements:** Parse historical strategy execution lines and calculate multi-tier statistical risk distributions (e.g., Win-Rate ratios, Maximum Peak-to-Trough Drawdown tracking, and Profit Factor metrics).

---

## 5. TECHNICAL AGENT SKILLS RUNTIME SPECIFICATIONS

### [SKILL 1]: ENVIRONMENT_SETUP
* **Objective:** Autonomously verify, install, and instantiate the development terminal layer on Windows hardware.
* **Algorithmic Sequence:**
  1. Scan host machine path routing environments to detect active installations of standard git and Linux-equivalent command terminals (Git Bash).
  2. If missing, automatically issue system execution commands to provision packages via local environment managers:
     ```dos
     winget install Git.Git --silent --accept-source-agreements --accept-package-agreements
     ```
  3. Initialize a clean local version control tracking tree (`git init`).
  4. Write the project `.gitignore` blueprint file executing explicit block filters on `.env`, `__pycache__/`, and `*.duckdb`.
  5. Construct the comprehensive 5-tier project directory structure outlined in Section 3.

### [SKILL 2]: GENERATE_MESSY_DATA
* **Objective:** Write custom Python scripts to populate structural data silos while programmatically embedding messy edge cases.
* **Code Design Constraints:**
  - Deploy Python's built-in file writing tools combined with structured fake dataset generators (Faker).
  - Enforce type coercion variances (e.g., occasionally converting floats to unformatted text lines).
  - Maintain precise mathematical relational integrity across files: ensure a percentage of generated transactions in Tenant A point to user records that do not exist, simulating structural database anomalies that require clean-up.

### [SKILL 3]: ETL_PROCESSING
* **Objective:** Ingest flat data streams and output normalized database files using optimal relational database techniques.
* **Technical Pipeline Standards:**
  - Execute data transformations using the DuckDB relational engine. Do not process datasets using standard in-memory structures like basic pandas DataFrames.
  - Write explicit SQL transformations using standard PostgreSQL syntax layout patterns.
  - Apply data cleaning techniques: implement explicit type casting routines (`CAST(date_column AS TIMESTAMP)`), handle null values with deterministic defaults (`COALESCE`), and filter out logic anomalies via explicit conditional parameters (`WHERE latency_ms < 60000`).
  - Consolidate individual tenant outputs into a unified relational schema using star schema modeling strategies (Fact and Dimension table formats), writing final outputs to `04_clean_data/analytics_production.duckdb`.

### [SKILL 4]: PRESENTATION_LAYER_DEPLOYMENT
* **Objective:** Construct a highly responsive local web interface to display both business insights and technical capabilities.
* **Interface Requirements:**
  - Build using Python's local Streamlit framework.
  - Implement a 6-tier sidebar multi-page layout mirroring the file structure in Section 3.
  - **Data Engineering Showcase (Critical Module):** Dedicate a visible view page specifically to showcasing data quality transformations. Render a split-screen viewport component displaying raw malformed tables side-by-side with processed DuckDB data assets. Document data anomalies caught and repaired by your pipeline to demonstrate engineering value to technical observers.

### [SKILL 5]: GITHUB_DEPLOYMENT_ENGINE
* **Objective:** Autonomously check local authentication, create a public origin repository under the user's personal GitHub account, and securely execute initial deployment routines.
* **Execution Sequence:**
  1. Check for the presence of the GitHub CLI tool (`gh`). If missing, issue the installation script terminal sequence: `winget install GitHub.cli`.
  2. Execute check on credential mapping state using `gh auth status`. Prompt user or pause if interaction is blocked.
  3. Programmatically generate a brand new, completely PUBLIC GitHub repository matching the official workspace name exactly:
     ```bash
     gh repo create ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE --public --description "Centralized enterprise data warehouse and business intelligence pipeline integrating multi-tenant microservice telemetry using DuckDB and Streamlit."
     ```
  4. Link the newly generated public URL tracking path to the local repository instance:
     ```bash
     git remote add origin https://github.com/<user_account_name>/ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE.git
     ```
  5. Perform the final stage deployment tracking verification sequence safely checking that all local rules specified in the `.gitignore` match perfectly:
     ```bash
     git add .
     git commit -m "Infrastructure Buildout: Established cross-platform schema boundaries, agent operational skill layers, and git staging rules."
     git branch -M main
     git push -u origin main
     ```

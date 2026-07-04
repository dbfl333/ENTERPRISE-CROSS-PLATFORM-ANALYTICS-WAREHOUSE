import streamlit as st
import os
import pandas as pd
import duckdb

st.set_page_config(page_title="Data Quality ETL - Showcase", layout="wide")

st.markdown("""
    <style>
    .showcase-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF8008, #FFC837);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .panel-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .metric-bubble {
        background: rgba(255, 128, 8, 0.1);
        border: 1px solid rgba(255, 128, 8, 0.3);
        border-radius: 5px;
        padding: 5px 10px;
        font-weight: 600;
        color: #FFC837;
        display: inline-block;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='showcase-header'>🛠️ Data Engineering & ETL Audit Showcase</h1>", unsafe_allow_html=True)
st.markdown("A split-screen diagnostic audit comparing messy raw source files directly with completed clean production data warehouse schemas.")

# Check database
db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ The production database `analytics_production.duckdb` was not found. Please run the ETL pipeline first to compile the data warehouse.")
    st.stop()

# Select Tenant for audit
tenant_select = st.sidebar.selectbox(
    "Select Tenant to Inspect",
    ["Tenant A: AI Markets Shop", "Tenant B: Agentic Prompt Labs", "Tenant C: Terrazas-home", "Tenant D: G-Trend Screener"]
)

conn = duckdb.connect(db_path, read_only=True)

if tenant_select == "Tenant A: AI Markets Shop":
    st.subheader("Tenant A: AI Markets Shop (E-Commerce Funnel)")
    
    st.markdown("""
    <div class='panel-card'>
        <h3>⚠️ Injected Raw Data Anomalies</h3>
        <ul>
            <li><b>Mixed Pricing Syntax:</b> Price strings formatted randomly as <code>$150.00</code>, <code>150</code>, or <code>150,00 USD</code>.</li>
            <li><b>Missing Geographic Identifiers:</b> Country fields left empty (null/blank) for 15% of records.</li>
            <li><b>Missing User Identifiers:</b> Abandoned checkout paths missing user ID references.</li>
            <li><b>Referential Integrity Errors:</b> 5% of transaction events mapped to random synthetic user keys not present in user directories.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Load raw
    raw_df = pd.read_csv("02_raw_data/shop_raw_sessions.csv", nrows=100)
    # Load clean
    clean_df = conn.execute("SELECT * FROM fact_shop_sessions LIMIT 100").df()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ❌ Raw Malformed Input (`02_raw_data/shop_raw_sessions.csv`)")
        st.dataframe(raw_df, use_container_width=True)
    with col2:
        st.markdown("####   Clean Data Warehouse (`fact_shop_sessions`)")
        st.dataframe(clean_df, use_container_width=True)
        
    st.markdown("""
    ### ⚙️ Transformation PostgreSQL SQL Engine Rule applied
    ```sql
    CAST(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(COALESCE(NULLIF(price_string, ''), '0'), '\\$', '', 'g'), 
                ' USD', '', 'g'
            ), 
            ',', '.', 'g'
        ) AS DECIMAL(10, 2)
    ) AS price,
    COALESCE(NULLIF(country, ''), 'Unknown') AS country,
    NULLIF(user_id, '') AS user_id
    ```
    """)

elif tenant_select == "Tenant B: Agentic Prompt Labs":
    st.subheader("Tenant B: Agentic Prompt Labs (LLM Logs)")
    
    st.markdown("""
    <div class='panel-card'>
        <h3>⚠️ Injected Raw Data Anomalies</h3>
        <ul>
            <li><b>Malformed JSON Strings:</b> Truncated JSON metadata configuration records (due to system cuts/token caps).</li>
            <li><b>System Hangs/Infinity Outliers:</b> Simulated runtime latency spikes exceeding 30,000ms.</li>
            <li><b>SaaS Rate Limit Bottlenecks:</b> Clusters of consecutive HTTP 429 status code requests.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Load raw
    raw_df = pd.read_csv("02_raw_data/prompt_raw_telemetry.csv", nrows=100)
    # Load clean
    clean_df = conn.execute("SELECT * FROM fact_prompt_telemetry LIMIT 100").df()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ❌ Raw Malformed Input (`02_raw_data/prompt_raw_telemetry.csv`)")
        st.dataframe(raw_df, use_container_width=True)
    with col2:
        st.markdown("####   Clean Data Warehouse (`fact_prompt_telemetry`)")
        st.dataframe(clean_df, use_container_width=True)
        
    st.markdown(r"""
    ### ⚙️ Transformation PostgreSQL SQL Engine Rule applied
    ```sql
    -- Filter out system latency outliers
    WHERE latency_ms < 60000
    
    -- Parse malformed JSON parameters using regex fallback
    COALESCE(REGEXP_EXTRACT(meta_json, '"model"\\s*:\\\s*"([^"]+)"', 1), 'Unknown') AS model,
    COALESCE(CAST(REGEXP_EXTRACT(meta_json, '"temperature"\\s*:\\\s*([0-9.]+)', 1) AS DOUBLE), 0.7) AS temperature
    ```
    """)

elif tenant_select == "Tenant C: Terrazas-home":
    st.subheader("Tenant C: Terrazas-home (Property Bookings)")
    
    st.markdown("""
    <div class='panel-card'>
        <h3>⚠️ Injected Raw Data Anomalies</h3>
        <ul>
            <li><b>Mixed Timestamp Standards:</b> Mixing standard dates with strings like <code>July 3rd, 2026</code>, <code>07/03/2026</code>, or <code>Friday, July 3rd, 2026</code>.</li>
            <li><b>Zero-Dollar Booking Discrepancies:</b> Confirmed active reservations listing booking total revenue as $0.00.</li>
            <li><b>Double Booking Errors:</b> Operational calendar conflicts where overlapping bookings occur on the same property.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Load raw
    raw_df = pd.read_csv("02_raw_data/terrazas_raw_bookings.csv", nrows=100)
    # Load clean
    clean_df = conn.execute("SELECT * FROM fact_terrazas_bookings LIMIT 100").df()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ❌ Raw Malformed Input (`02_raw_data/terrazas_raw_bookings.csv`)")
        st.dataframe(raw_df, use_container_width=True)
    with col2:
        st.markdown("####   Clean Data Warehouse (`fact_terrazas_bookings`)")
        st.dataframe(clean_df, use_container_width=True)
        
    st.markdown("""
    ### ⚙️ Transformation PostgreSQL SQL Engine Rule applied
    ```sql
    -- Mixed check-in and check-out timestamp standardization using regex cleaning
    CASE 
        WHEN check_in LIKE '%/%/%' THEN strptime(check_in, '%m/%d/%Y')::DATE
        WHEN check_in SIMILAR TO '[0-9]{4}-[0-9]{2}-[0-9]{2}' THEN CAST(check_in AS DATE)
        ELSE strptime(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(check_in, '^(Monday|Tuesday|...)...'), ...), ...), '%B %d, %Y')::DATE
    END AS check_in
    
    -- Zero-Dollar correction using base rates and duration multiplier
    CASE WHEN raw_amount = 0.00 AND status != 'Cancelled' THEN base_rate * DATEDIFF('day', check_in, check_out) * seasonal_mult ELSE raw_amount END
    
    -- Flag double bookings using check overlap validation logic
    EXISTS (
        SELECT 1 FROM clean_bookings t2 
        WHERE t1.property_id = t2.property_id AND t1.booking_id != t2.booking_id 
        AND t1.check_in < t2.check_out AND t2.check_in < t1.check_out
    ) AS is_double_booked
    ```
    """)

elif tenant_select == "Tenant D: G-Trend Screener":
    st.subheader("Tenant D: G-Trend Screener (Financial Strategy Trades)")
    
    st.markdown("""
    <div class='panel-card'>
        <h3>🛡️ Data Source Integrity</h3>
        <p>No synthetic faker values are generated for this tenant. This layer acts as a direct integration porting quantitative trading backtest performance records from TradingView strategies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load raw
    raw_df = pd.read_csv("02_raw_data/gtrend_raw_backtests.csv", nrows=100)
    # Load clean
    clean_df = conn.execute("SELECT * FROM fact_gtrend_trades LIMIT 100").df()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📁 Raw Integrated CSV (`02_raw_data/gtrend_raw_backtests.csv`)")
        st.dataframe(raw_df, use_container_width=True)
    with col2:
        st.markdown("####   Clean Data Warehouse (`fact_gtrend_trades`)")
        st.dataframe(clean_df, use_container_width=True)
        
    st.markdown("""
    ### ⚙️ Ingestion & Metric Calculations
    ```sql
    -- Import CSV and calculate trade duration metrics in hours
    CREATE TABLE fact_gtrend_trades AS
    SELECT
        trade_id,
        asset_pair,
        CAST(entry_timestamp AS TIMESTAMP) AS entry_timestamp,
        CAST(exit_timestamp AS TIMESTAMP) AS exit_timestamp,
        position_type_long_short AS position_type,
        CAST(profit_loss_percentage AS DOUBLE) AS profit_loss_percentage,
        CAST(max_drawdown_percentage AS DOUBLE) AS max_drawdown_percentage,
        DATEDIFF('minute', CAST(entry_timestamp AS TIMESTAMP), CAST(exit_timestamp AS TIMESTAMP)) / 60.0 AS duration_hours
    FROM read_csv_auto('02_raw_data/gtrend_raw_backtests.csv');
    ```
    """)

conn.close()

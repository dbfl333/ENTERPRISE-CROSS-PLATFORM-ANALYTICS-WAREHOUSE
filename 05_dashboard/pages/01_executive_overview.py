import streamlit as st
import os
import duckdb
import pandas as pd

st.set_page_config(page_title="Executive Overview - Analytics Warehouse", layout="wide")

st.markdown("""
    <style>
    .kpi-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(125, 42, 232, 0.4);
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #B2B2B2;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00E5FF;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Executive Operations Overview")
st.markdown("Consolidated real-time KPIs and system operational integrity dashboards across all business tenants.")

db_path = "04_clean_data/analytics_production.duckdb"

if not os.path.exists(db_path):
    st.warning("⚠️ The production database `analytics_production.duckdb` was not found. Please run the ETL pipeline first to compile the data warehouse.")
    st.stop()

# Connect to DuckDB
conn = duckdb.connect(db_path, read_only=True)

# Fetch KPIs
try:
    # Tenant A KPIs
    shop_kpis = conn.execute("""
        SELECT 
            COUNT(DISTINCT session_id) as total_sessions,
            SUM(price) FILTER(WHERE funnel_stage = 'Checkout Success') as total_revenue,
            (COUNT(DISTINCT session_id) FILTER(WHERE funnel_stage = 'Checkout Success') * 100.0 / COUNT(DISTINCT session_id)) as conv_rate
        FROM fact_shop_sessions
    """).fetchone()

    # Tenant B KPIs
    prompt_kpis = conn.execute("""
        SELECT 
            COUNT(*) as total_requests,
            AVG(latency_ms) as avg_latency,
            SUM(total_token_count) as total_tokens,
            (COUNT(*) FILTER(WHERE http_status_code = 429) * 100.0 / COUNT(*)) as rate_limit_pct
        FROM fact_prompt_telemetry
    """).fetchone()

    # Tenant C KPIs
    terrazas_kpis = conn.execute("""
        SELECT 
            COUNT(*) as total_bookings,
            SUM(total_amount) FILTER(WHERE status != 'Cancelled') as total_rev,
            COUNT(*) FILTER(WHERE is_double_booked = TRUE) as conflict_count
        FROM fact_terrazas_bookings
    """).fetchone()

    # Tenant D KPIs
    gtrend_kpis = conn.execute("""
        SELECT 
            COUNT(*) as total_trades,
            AVG(profit_loss_percentage) as avg_pl,
            (COUNT(*) FILTER(WHERE profit_loss_percentage > 0) * 100.0 / COUNT(*)) as win_rate
        FROM fact_gtrend_trades
    """).fetchone()

except Exception as e:
    st.error(f"Error querying data warehouse schema: {e}")
    st.stop()

# Render KPI Columns
st.subheader("Tenant Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Tenant A: Shop Revenue</div>
        <div class='kpi-val'>${shop_kpis[1]:,.2f}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Funnel Conv: {shop_kpis[2]:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Tenant B: Prompt Logs</div>
        <div class='kpi-val'>{prompt_kpis[0]:,}</div>
        <div style='color: #FFB300; font-size: 0.85rem;'>Rate Limits (429): {prompt_kpis[3]:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Tenant C: Hotel Bookings</div>
        <div class='kpi-val'>${terrazas_kpis[1]:,.2f}</div>
        <div style='color: #FF3333; font-size: 0.85rem;'>Overlaps Flagged: {terrazas_kpis[2]}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Tenant D: Quantitative Trades</div>
        <div class='kpi-val'>{gtrend_kpis[0]}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Trade Win Rate: {gtrend_kpis[2]:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Visualizations Layout
st.subheader("Unified Revenue & Metric Trends")

c1, c2 = st.columns(2)

with c1:
    # Cumulative revenues over months
    shop_monthly = conn.execute("""
        SELECT 
            STRFTIME(event_timestamp, '%Y-%m') as month, 
            SUM(price) as rev 
        FROM fact_shop_sessions 
        WHERE funnel_stage = 'Checkout Success'
        GROUP BY 1 ORDER BY 1
    """).df()
    
    st.markdown("#### Tenant A Monthly Checkout Revenue")
    st.line_chart(shop_monthly.set_index("month"))

with c2:
    # Prompt token volume trends
    prompt_monthly = conn.execute("""
        SELECT 
            STRFTIME(log_timestamp, '%Y-%m') as month, 
            SUM(total_token_count) as tokens 
        FROM fact_prompt_telemetry 
        GROUP BY 1 ORDER BY 1
    """).df()
    
    st.markdown("#### Tenant B Monthly LLM Token Throughput")
    st.bar_chart(prompt_monthly.set_index("month"))

conn.close()

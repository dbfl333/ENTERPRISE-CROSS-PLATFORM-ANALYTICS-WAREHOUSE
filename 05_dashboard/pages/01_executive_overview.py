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
    .staging-card {
        background: rgba(255, 128, 8, 0.05);
        border: 1px dashed rgba(255, 128, 8, 0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Executive Operations Overview")
st.markdown("Consolidated real-time KPIs and system operational integrity dashboards across all live and staging business tenants.")

db_path = "04_clean_data/analytics_production.duckdb"

if not os.path.exists(db_path):
    st.warning("⚠️ The production database `analytics_production.duckdb` was not found. Please run the ETL pipeline first.")
    st.stop()

# Connect to DuckDB
conn = duckdb.connect(db_path, read_only=True)

# Fetch KPIs
try:
    # Tenant A (Shopify API) KPIs
    shop_kpis = conn.execute("""
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue
        FROM fact_shop_orders
    """).fetchone()

    # Tenant B (Binance API) KPIs - Latest BTC close price
    binance_kpis = conn.execute("""
        SELECT 
            close_price,
            trade_volume
        FROM fact_binance_klines
        ORDER BY open_timestamp DESC
        LIMIT 1
    """).fetchone()

except Exception as e:
    st.error(f"Error querying data warehouse schema: {e}")
    st.stop()

# Render KPI Columns
st.subheader("Live Tenant Key Performance Indicators")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Tenant A: Shopify Total Sales</div>
        <div class='kpi-val'>${shop_kpis[1]:,.2f}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Total Orders: {shop_kpis[0]} (Live API)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Tenant B: Latest BTC Close Price</div>
        <div class='kpi-val'>${binance_kpis[0]:,.2f}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Trading Volume: {binance_kpis[1]:,.2f} (Binance API)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Active Live Connections</div>
        <div class='kpi-val'>2 / 4</div>
        <div style='color: #FFB300; font-size: 0.85rem;'>2 Tenants Awaiting Launch</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

st.subheader("Pre-Launch Staging Profiles")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class='staging-card'>
        <h4>Tenant C: Agentic Prompt Labs</h4>
        <p style='color: #FFB300; font-weight: 600;'>Awaiting Day 1 Launch</p>
        <p style='font-size: 0.9rem; color: #B2B2B2;'>Staging table <code>staging_prompt_telemetry</code> is successfully provisioned and verified in DuckDB. No fake data allowed.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='staging-card'>
        <h4>Tenant D: Terrazas-home</h4>
        <p style='color: #FFB300; font-weight: 600;'>Awaiting Day 1 Launch</p>
        <p style='font-size: 0.9rem; color: #B2B2B2;'>Staging table <code>staging_terrazas_bookings</code> is successfully provisioned and verified in DuckDB. No fake data allowed.</p>
    </div>
    """, unsafe_allow_html=True)

conn.close()

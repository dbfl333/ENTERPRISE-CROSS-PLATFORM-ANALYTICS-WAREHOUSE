import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="Executive Overview", layout="wide")
st.title("Executive Operations Overview")
st.markdown("**LIVE PRODUCTION DATA** | Aggregation of all 4 tenant endpoints.")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Multi-Tenant Unified DuckDB Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'

@st.cache_data(ttl=300)
def load_kpis():
    conn = duckdb.connect(DB_PATH, read_only=True)
    shop = conn.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM fact_shop_orders").fetchone()
    binance = conn.execute("SELECT close_price, fng_value, fng_classification FROM fact_binance_klines ORDER BY open_timestamp DESC LIMIT 1").fetchone()
    prompt = conn.execute("SELECT COUNT(*), AVG(search_interest_score) FROM staging_prompt_telemetry").fetchone()
    terrazas = conn.execute("SELECT COUNT(*), COALESCE(SUM(total_gross_amount), 0) FROM staging_terrazas_bookings").fetchone()
    conn.close()
    return shop, binance, prompt, terrazas

try:
    shop, binance, prompt, terrazas = load_kpis()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AI Shop Rev (Shopify)", f"${shop[1]:,.2f}")
    if binance:
        c2.metric("BTC (Binance)", f"${binance[0]:,.2f}", binance[2])
    c3.metric("Prompt API (GitHub)", f"{prompt[0]} reqs")
    c4.metric("Terrazas (Bookings)", f"${terrazas[1]:,.2f}")
    
    st.write("---")
    st.subheader("Raw SQL Viewer")
    with st.expander("View Enterprise KPIs Data"):
        conn = duckdb.connect(DB_PATH, read_only=True)
        st.write("**fact_shop_orders**")
        st.dataframe(conn.execute("SELECT * FROM fact_shop_orders LIMIT 100").df(), use_container_width=True)
        conn.close()
except Exception as e:
    st.error(f"Error loading data: {e}")

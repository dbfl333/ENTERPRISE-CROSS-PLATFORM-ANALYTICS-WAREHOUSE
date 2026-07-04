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
    
    # Load some real data for overview charts
    shop_df = conn.execute("SELECT created_at, total_amount FROM fact_shop_orders").df()
    binance_df = conn.execute("SELECT open_timestamp, close_price FROM fact_binance_klines ORDER BY open_timestamp DESC LIMIT 100").df()
    
    conn.close()
    return shop, binance, prompt, terrazas, shop_df, binance_df

try:
    shop, binance, prompt, terrazas, shop_df, binance_df = load_kpis()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AI Shop Rev (Shopify)", f"${shop[1]:,.2f}")
    if binance:
        c2.metric("BTC (Binance)", f"${binance[0]:,.2f}", binance[2])
    c3.metric("Prompt API (GitHub)", f"{prompt[0]} reqs")
    c4.metric("Terrazas (Bookings)", f"${terrazas[1]:,.2f}")
    
    st.write("---")
    st.subheader("High-Level Global Metrics")
    col_a, col_b = st.columns(2)
    
    with col_a:
        if not shop_df.empty:
            c = alt.Chart(shop_df).mark_line().encode(x='created_at', y='total_amount').properties(height=200, title="Shopify Revenue Timeline")
            st.altair_chart(c, use_container_width=True)
            
    with col_b:
        if not binance_df.empty:
            c = alt.Chart(binance_df).mark_area(opacity=0.5, color='orange').encode(x='open_timestamp', y=alt.Y('close_price', scale=alt.Scale(zero=False))).properties(height=200, title="BTC Price Action")
            st.altair_chart(c, use_container_width=True)

    st.write("---")
    st.subheader("Raw SQL Viewer (PII Scrubbed)")
    with st.expander("View Enterprise KPIs Data"):
        conn = duckdb.connect(DB_PATH, read_only=True)
        st.write("**fact_shop_orders**")
        df = conn.execute("SELECT * FROM fact_shop_orders LIMIT 100").df()
        # Drop PII
        cols_to_drop = [c for c in df.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
        df = df.drop(columns=cols_to_drop)
        st.dataframe(df, use_container_width=True)
        conn.close()
except Exception as e:
    st.error(f"Error loading data: {e}")

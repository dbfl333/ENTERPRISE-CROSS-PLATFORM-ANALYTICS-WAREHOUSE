import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AI MARKETS SHOP", layout="wide")
st.title("AI MARKETS SHOP")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Shopify Admin API & GeoJS")

DB_PATH = '04_clean_data/analytics_production.duckdb'

conn = duckdb.connect(DB_PATH, read_only=True)
df_orders = conn.execute("SELECT * FROM fact_shop_orders").df()
df_ga4 = conn.execute("SELECT * FROM staging_ga4_sessions").df()
conn.close()

st.subheader("Order Metrics Visualized")
c1, c2, c3 = st.columns(3)

with c1:
    if 'financial_status' in df_orders.columns:
        status_chart = alt.Chart(df_orders).mark_arc().encode(theta='count()', color='financial_status').properties(height=200, title="Financial Status")
        st.altair_chart(status_chart, use_container_width=True)

with c2:
    if 'total_amount' in df_orders.columns:
        hist_chart = alt.Chart(df_orders).mark_bar().encode(alt.X('total_amount', bin=True), y='count()').properties(height=200, title="Order Value Distribution")
        st.altair_chart(hist_chart, use_container_width=True)

with c3:
    if 'created_at' in df_orders.columns and 'total_amount' in df_orders.columns:
        time_chart = alt.Chart(df_orders).mark_line(color='green').encode(x='created_at', y='total_amount').properties(height=200, title="Revenue Timeline")
        st.altair_chart(time_chart, use_container_width=True)

st.subheader("GA4 Traffic Overlay")
c4, c5 = st.columns(2)
with c4:
    if not df_ga4.empty:
        device_chart = alt.Chart(df_ga4).mark_bar().encode(x='device_category', y='count()', color='device_category').properties(height=200, title="Device Traffic")
        st.altair_chart(device_chart, use_container_width=True)

with c5:
    if not df_ga4.empty:
        country_chart = alt.Chart(df_ga4).mark_arc(innerRadius=40).encode(theta='count()', color='country').properties(height=200, title="Global Reach")
        st.altair_chart(country_chart, use_container_width=True)

st.write("---")
st.subheader("Raw SQL Data Viewer (PII Scrubbed)")
with st.expander("View Shopify Funnel SQL Ledger"):
    cols_to_drop = [c for c in df_orders.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df_orders.drop(columns=cols_to_drop), use_container_width=True)

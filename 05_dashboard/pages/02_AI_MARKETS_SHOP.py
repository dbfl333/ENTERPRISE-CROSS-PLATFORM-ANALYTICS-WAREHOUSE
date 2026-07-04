import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AI MARKETS SHOP", layout="wide")
st.title("AI MARKETS SHOP")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync1"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Orders & GA4 ---
st.write("---")
st.subheader("Source 1: Core Shopify Revenue & Web Traffic")
st.markdown("> **Strategic Value:** Raw financial throughput combined with GA4 session telemetry.")
df_orders = conn.execute("SELECT * FROM fact_shop_orders").df()
df_ga4 = conn.execute("SELECT * FROM staging_ga4_sessions").df()

c1, c2, c3 = st.columns(3)
with c1:
    if 'total_price' in df_orders.columns:
        c = alt.Chart(df_orders).mark_bar().encode(alt.X('total_price', bin=True), y='count()').properties(height=200, title="Order Values")
        st.altair_chart(c, use_container_width=True)
with c2:
    if 'created_at' in df_orders.columns and 'total_price' in df_orders.columns:
        c = alt.Chart(df_orders).mark_line().encode(x='created_at', y='total_price').properties(height=200, title="Revenue Timeline")
        st.altair_chart(c, use_container_width=True)
with c3:
    if not df_ga4.empty:
        c = alt.Chart(df_ga4).mark_arc(innerRadius=40).encode(theta='count()', color='device_category').properties(height=200, title="GA4 Traffic Device")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: Forex Rates ---
st.write("---")
st.subheader("Source 2: Global Macro (Frankfurter FX Rates)")
st.markdown("> **Strategic Value:** Adjusting regional ad-spend based on currency purchasing power parity.")
df_fx = conn.execute("SELECT * FROM ext_shop_forex").df()
if not df_fx.empty:
    c1, c2 = st.columns(2)
    with c1:
        c = alt.Chart(df_fx).mark_line(color='green').encode(x='date', y='rate_EUR').properties(height=200, title="EUR Exchange Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_fx).mark_line(color='blue').encode(x='date', y='rate_GBP').properties(height=200, title="GBP Exchange Rate")
        st.altair_chart(c, use_container_width=True)

# --- Source 3: Buyer Geo ---
st.write("---")
st.subheader("Source 3: Geographic Concentration (GeoJS)")
st.markdown("> **Strategic Value:** Identifying high-density buyer locations for targeted Meta/Facebook Ads.")
df_geo = conn.execute("SELECT * FROM ext_shop_buyer_geo").df()
if not df_geo.empty:
    c = alt.Chart(df_geo).mark_bar().encode(x='country', y='count()', color='city').properties(height=200, title="Geographic Distribution")
    st.altair_chart(c, use_container_width=True)

# --- Source 4: Wikipedia Trends ---
st.write("---")
st.subheader("Source 4: Macro Narrative (Wikimedia Pageviews)")
st.markdown("> **Strategic Value:** Gauging mainstream interest in 'Artificial Intelligence' to time massive email blasts.")
df_wiki = conn.execute("SELECT * FROM ext_shop_wikipedia").df()
if not df_wiki.empty:
    c = alt.Chart(df_wiki).mark_area(opacity=0.5, color='orange').encode(x='timestamp', y='views').properties(height=200, title="Wikipedia Topic Views")
    st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander (PII Scrubbed) ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Core Orders")
    drop_cols = [c for c in df_orders.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df_orders.drop(columns=drop_cols), use_container_width=True)
    st.write("Forex Rates")
    st.dataframe(df_fx, use_container_width=True)
    st.write("Geographic Data")
    drop_cols = [c for c in df_geo.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df_geo.drop(columns=drop_cols), use_container_width=True)
    st.write("Wikipedia Data")
    st.dataframe(df_wiki, use_container_width=True)
conn.close()

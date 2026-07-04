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
df_orders = conn.execute("SELECT * FROM fact_shop_orders").df()
df_ga4 = conn.execute("SELECT * FROM staging_ga4_sessions").df()
df_fx = conn.execute("SELECT * FROM ext_shop_forex").df()
df_geo = conn.execute("SELECT * FROM ext_shop_buyer_geo").df()
df_wiki = conn.execute("SELECT * FROM ext_shop_wikipedia").df()
df_trends = conn.execute("SELECT * FROM ext_shop_google_trends").df()
conn.close()

# Remove PII
drop_cols_orders = [c for c in df_orders.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
df_orders_clean = df_orders.drop(columns=drop_cols_orders)
drop_cols_geo = [c for c in df_geo.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
df_geo_clean = df_geo.drop(columns=drop_cols_geo)

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Orders & GA4 ---
st.write("---")
st.subheader("Source 1: Core Shopify Revenue & Web Traffic")
st.markdown("> **Strategic Value:** Raw financial throughput combined with GA4 session telemetry.")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if 'total_price' in df_orders.columns:
        c = alt.Chart(df_orders).mark_bar().encode(alt.X('total_price', bin=True), y='count()').properties(height=150, title="Order Values")
        st.altair_chart(c, use_container_width=True)
with c2:
    if 'created_at' in df_orders.columns and 'total_price' in df_orders.columns:
        c = alt.Chart(df_orders).mark_line().encode(x='created_at', y='total_price').properties(height=150, title="Revenue Timeline")
        st.altair_chart(c, use_container_width=True)
with c3:
    if not df_ga4.empty:
        c = alt.Chart(df_ga4).mark_arc(innerRadius=40).encode(theta='count()', color='device_category').properties(height=150, title="Device Traffic")
        st.altair_chart(c, use_container_width=True)
with c4:
    if not df_ga4.empty:
        c = alt.Chart(df_ga4).mark_bar().encode(x='session_source', y='count()', color='session_source').properties(height=150, title="Traffic Sources")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data (PII Scrubbed):**")
st.dataframe(df_orders_clean, use_container_width=True, height=130)

# --- Source 2: Forex Rates ---
st.write("---")
st.subheader("Source 2: Global Macro (Frankfurter FX Rates)")
st.markdown("> **Strategic Value:** Adjusting regional ad-spend based on currency purchasing power parity.")
c1, c2, c3 = st.columns(3)
if not df_fx.empty:
    with c1:
        c = alt.Chart(df_fx).mark_line(color='green').encode(x='date', y='rate_EUR').properties(height=150, title="EUR Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_fx).mark_line(color='blue').encode(x='date', y='rate_GBP').properties(height=150, title="GBP Rate")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_fx).mark_area(color='purple', opacity=0.3).encode(x='date', y='rate_MXN').properties(height=150, title="MXN Volatility")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_fx, use_container_width=True, height=130)

# --- Source 3: Buyer Geo ---
st.write("---")
st.subheader("Source 3: Geographic Concentration (GeoJS)")
st.markdown("> **Strategic Value:** Identifying high-density buyer locations for targeted Meta/Facebook Ads.")
c1, c2 = st.columns(2)
if not df_geo.empty:
    with c1:
        c = alt.Chart(df_geo).mark_bar().encode(x='country', y='count()', color='city').properties(height=150, title="Geo Distribution")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_geo).mark_arc().encode(theta='count()', color='timezone').properties(height=150, title="Timezone Spread")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data (PII Scrubbed):**")
st.dataframe(df_geo_clean, use_container_width=True, height=130)

# --- Source 4: Wikipedia Trends ---
st.write("---")
st.subheader("Source 4: Macro Narrative (Wikimedia Pageviews)")
st.markdown("> **Strategic Value:** Gauging mainstream interest in 'Artificial Intelligence' to time massive email blasts.")
c1, c2 = st.columns(2)
if not df_wiki.empty:
    with c1:
        c = alt.Chart(df_wiki).mark_area(opacity=0.5, color='orange').encode(x='timestamp', y='views').properties(height=150, title="Topic Views")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_wiki).mark_bar(color='gray').encode(x='article', y='views').properties(height=150, title="Article Comparison")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_wiki, use_container_width=True, height=130)

# --- Source 5: Google Trends ---
st.write("---")
st.subheader("Source 5: Google Trends (E-Commerce Interest & Related Trends)")
st.markdown("> **Strategic Value:** Identifying keyword search momentum and search query intentions on Google.")
c1, c2, c3 = st.columns(3)
if not df_trends.empty:
    with c1:
        c = alt.Chart(df_trends).mark_line(color='blue').encode(x='search_date:T', y='search_interest_score', color='keyword_tracked').properties(height=150, title="Search Interest Score")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_trends).mark_bar().encode(x='keyword_tracked', y='mean(weekly_momentum_pct)', color='keyword_tracked').properties(height=150, title="Avg Weekly Momentum")
        st.altair_chart(c, use_container_width=True)
    with c3:
        st.write("**Related Queries:**")
        for idx, row in df_trends.head(3).iterrows():
            st.markdown(f"- **{row['keyword_tracked']}**: `{row['top_related_query_1']}` (Rising: `{row['rising_query_1']}`)")
st.write("**Raw Google Trends Data:**")
st.dataframe(df_trends, use_container_width=True, height=130)

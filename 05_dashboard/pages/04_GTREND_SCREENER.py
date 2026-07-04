import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="GTREND SCREENER", layout="wide")
st.title("GTREND SCREENER")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Binance API")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df = conn.execute("SELECT * FROM fact_binance_klines ORDER BY open_timestamp ASC").df()
conn.close()

st.subheader("Quantitative Market Telemetry")
c1, c2 = st.columns(2)

with c1:
    if not df.empty:
        price_chart = alt.Chart(df).mark_line(color='gold').encode(x='open_timestamp', y=alt.Y('close_price', scale=alt.Scale(zero=False))).properties(height=250, title="Asset Closing Price")
        st.altair_chart(price_chart, use_container_width=True)

with c2:
    if not df.empty:
        vol_chart = alt.Chart(df).mark_bar(opacity=0.6).encode(x='open_timestamp', y='volume').properties(height=250, title="Market Volume")
        st.altair_chart(vol_chart, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    if 'fng_value' in df.columns:
        fng_chart = alt.Chart(df).mark_area(color='purple', opacity=0.3).encode(x='open_timestamp', y='fng_value').properties(height=250, title="Fear & Greed Index Tracking")
        st.altair_chart(fng_chart, use_container_width=True)
with c4:
    if 'rsi_14' in df.columns:
        rsi_chart = alt.Chart(df).mark_line(color='cyan').encode(x='open_timestamp', y='rsi_14').properties(height=250, title="RSI (14 Period)")
        st.altair_chart(rsi_chart, use_container_width=True)

st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Binance Klines SQL Data"):
    st.dataframe(df, use_container_width=True)

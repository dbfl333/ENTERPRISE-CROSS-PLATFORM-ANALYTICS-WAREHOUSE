import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="GTREND SCREENER", layout="wide")
st.title("GTREND SCREENER")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync2"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Binance Klines ---
st.write("---")
st.subheader("Source 1: Core Market Action (Binance WebSocket)")
st.markdown("> **Strategic Value:** Immediate price, RSI, and volume profiling for algorithmic screener targets.")
df_klines = conn.execute("SELECT * FROM fact_binance_klines").df()
c1, c2 = st.columns(2)
with c1:
    if not df_klines.empty:
        c = alt.Chart(df_klines).mark_line(color='gold').encode(x='open_timestamp', y=alt.Y('close_price', scale=alt.Scale(zero=False))).properties(height=200, title="Price Action")
        st.altair_chart(c, use_container_width=True)
with c2:
    if not df_klines.empty:
        c = alt.Chart(df_klines).mark_bar(opacity=0.6).encode(x='open_timestamp', y='volume').properties(height=200, title="Volume Profile")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: CoinGecko Bitcoin Trends ---
st.write("---")
st.subheader("Source 2: Broad Crypto Trends (CoinGecko)")
st.markdown("> **Strategic Value:** Identifying which altcoins are surging alongside BTC for narrative-based portfolio rotation.")
df_cg = conn.execute("SELECT * FROM ext_binance_btc").df()
if not df_cg.empty:
    c = alt.Chart(df_cg).mark_bar().encode(x='symbol', y='score', color='symbol').properties(height=200, title="CoinGecko Trending Score")
    st.altair_chart(c, use_container_width=True)

# --- Source 3: Fear & Greed ---
st.write("---")
st.subheader("Source 3: Market Sentiment (Alternative.me)")
st.markdown("> **Strategic Value:** Rebalancing portfolio risk parameters based on extreme psychological readings.")
df_fng = conn.execute("SELECT * FROM ext_crypto_sentiment").df()
if not df_fng.empty:
    c = alt.Chart(df_fng).mark_line(color='purple').encode(x='timestamp', y='value').properties(height=200, title="Fear & Greed Index")
    st.altair_chart(c, use_container_width=True)

# --- Source 4: Blockchain Network Stats ---
st.write("---")
st.subheader("Source 4: On-Chain Health (Blockchain.info)")
st.markdown("> **Strategic Value:** Validating market moves against actual miner hash-rate and network fee accumulation.")
df_bc = conn.execute("SELECT * FROM ext_blockchain_network").df()
if not df_bc.empty:
    c1, c2 = st.columns(2)
    with c1:
        c = alt.Chart(df_bc).mark_area(color='cyan', opacity=0.3).encode(x='timestamp', y='hash_rate').properties(height=200, title="Network Hash Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_bc).mark_line(color='red').encode(x='timestamp', y='total_fees_btc').properties(height=200, title="Total Network Fees (BTC)")
        st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Klines Data"); st.dataframe(df_klines, use_container_width=True)
    st.write("CoinGecko Data"); st.dataframe(df_cg, use_container_width=True)
    st.write("Sentiment Data"); st.dataframe(df_fng, use_container_width=True)
    st.write("On-Chain Data"); st.dataframe(df_bc, use_container_width=True)
conn.close()

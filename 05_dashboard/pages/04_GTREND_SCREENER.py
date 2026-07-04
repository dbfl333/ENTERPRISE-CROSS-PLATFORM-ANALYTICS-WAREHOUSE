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
df_klines = conn.execute("SELECT * FROM fact_binance_klines").df()
df_cg = conn.execute("SELECT * FROM ext_binance_btc").df()
df_fng = conn.execute("SELECT * FROM ext_crypto_sentiment").df()
df_bc = conn.execute("SELECT * FROM ext_blockchain_network").df()
df_trends = conn.execute("SELECT * FROM ext_gtrend_google_trends").df()
conn.close()

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Binance Klines ---
st.write("---")
st.subheader("Source 1: Core Market Action (Binance WebSocket)")
st.markdown("> **Strategic Value:** Immediate price, RSI, and volume profiling for algorithmic screener targets.")
c1, c2, c3 = st.columns(3)
if not df_klines.empty:
    with c1:
        c = alt.Chart(df_klines).mark_line(color='gold').encode(x='open_time', y=alt.Y('last_price', scale=alt.Scale(zero=False))).properties(height=150, title="Price Action")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_klines).mark_bar(opacity=0.6).encode(x='open_time', y='volume').properties(height=150, title="Volume Profile")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_klines).mark_area(color='purple', opacity=0.4).encode(x='open_time', y='count').properties(height=150, title="Trade Count Velocity")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_klines, use_container_width=True, height=130)

# --- Source 2: CoinGecko Bitcoin Trends ---
st.write("---")
st.subheader("Source 2: Broad Crypto Trends (CoinGecko)")
st.markdown("> **Strategic Value:** Identifying which altcoins are surging alongside BTC for narrative-based portfolio rotation.")
c1, c2 = st.columns(2)
if not df_cg.empty:
    with c1:
        c = alt.Chart(df_cg).mark_bar().encode(x='symbol', y='score', color='symbol').properties(height=150, title="Trending Score")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_cg).mark_point(filled=True, size=100).encode(x='market_cap_rank', y='price_btc', color='symbol').properties(height=150, title="Rank vs BTC Price")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_cg, use_container_width=True, height=130)

# --- Source 3: Fear & Greed ---
st.write("---")
st.subheader("Source 3: Market Sentiment (Alternative.me)")
st.markdown("> **Strategic Value:** Rebalancing portfolio risk parameters based on extreme psychological readings.")
c1, c2 = st.columns(2)
if not df_fng.empty:
    with c1:
        c = alt.Chart(df_fng).mark_line(color='red').encode(x='timestamp', y='value').properties(height=150, title="Fear & Greed Index")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_fng).mark_arc().encode(theta='count()', color='value_classification').properties(height=150, title="Classification Mix")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_fng, use_container_width=True, height=130)

# --- Source 4: Blockchain Network Stats ---
st.write("---")
st.subheader("Source 4: On-Chain Health (Blockchain.info)")
st.markdown("> **Strategic Value:** Validating market moves against actual miner hash-rate and network fee accumulation.")
c1, c2, c3 = st.columns(3)
if not df_bc.empty:
    with c1:
        c = alt.Chart(df_bc).mark_area(color='cyan', opacity=0.3).encode(x='timestamp', y='hash_rate').properties(height=150, title="Network Hash Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_bc).mark_line(color='orange').encode(x='timestamp', y='total_fees_btc').properties(height=150, title="Total Network Fees (BTC)")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_bc).mark_bar(color='brown').encode(x='timestamp', y='minutes_between_blocks').properties(height=150, title="Block Time (Mins)")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_bc, use_container_width=True, height=130)

# --- Source 5: Google Trends ---
st.write("---")
st.subheader("Source 5: Google Trends (Crypto Interest & Related Trends)")
st.markdown("> **Strategic Value:** Evaluating Google retail search query momentum to capture breakout interest waves.")
c1, c2, c3 = st.columns(3)
if not df_trends.empty:
    with c1:
        c = alt.Chart(df_trends).mark_line(color='green').encode(x='search_date:T', y='search_interest_score', color='keyword_tracked').properties(height=150, title="Search Interest Score")
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

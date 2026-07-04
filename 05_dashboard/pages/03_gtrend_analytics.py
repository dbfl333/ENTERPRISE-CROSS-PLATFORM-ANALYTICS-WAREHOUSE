import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="G-Trend Screener - Binance Market", layout="wide")

st.sidebar.header("📊 Market Selector")
selected_symbol = st.sidebar.selectbox("Select Asset Pair", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

st.title(f"📈 {selected_symbol} Market Data & Screener")
st.markdown(f"Historical {selected_symbol} daily candlestick indicators, network metrics, and live strategy evaluations.")

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()


@st.cache_data
def load_latest_signal(symbol):
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute(f"""
        SELECT close_price, rsi_14, macd_line, macd_signal, sma_20, sma_50,
               screener_good_pair_flag, timestamp_fetched, daily_change_percent, volatility_index,
               fng_value, fng_classification, btc_hash_rate, btc_market_price_usd
        FROM fact_binance_klines
        WHERE symbol = '{symbol}'
        ORDER BY open_timestamp DESC
        LIMIT 1
    """).fetchone()
    conn.close()
    return result


@st.cache_data
def load_pair_stats(symbol):
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute(f"""
        SELECT COUNT(*) as total_candles, AVG(close_price) as avg_close,
               MAX(high_price) as max_high, MIN(low_price) as min_low
        FROM fact_binance_klines
        WHERE symbol = '{symbol}'
    """).fetchone()
    conn.close()
    return result


@st.cache_data
def load_candles(symbol):
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute(f"""
        SELECT open_timestamp as date, open_price, high_price, low_price,
               close_price, trade_volume, sma_20, sma_50, rsi_14
        FROM fact_binance_klines
        WHERE symbol = '{symbol}'
        ORDER BY open_timestamp ASC
    """).df()
    conn.close()
    return df


@st.cache_data
def load_trending_narratives():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT trending_coin_name as name, trending_coin_symbol as symbol, 1.0 AS weight FROM fact_binance_klines").df()
    conn.close()
    # Unique coins
    df = df.drop_duplicates(subset=["name"])
    return df


@st.cache_data
def load_ledger(symbol):
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute(f"""
        SELECT open_timestamp, open_price, high_price, low_price, close_price,
               trade_volume, rsi_14, macd_line, macd_signal, sma_20, sma_50,
               daily_change_percent, volatility_index, fng_value, fng_classification,
               btc_hash_rate, btc_market_price_usd
        FROM fact_binance_klines
        WHERE symbol = '{symbol}'
        ORDER BY open_timestamp DESC
        LIMIT 100
    """).df()
    conn.close()
    return df


stats = load_pair_stats(selected_symbol)

# ==================== TIER 1: VISUAL METRIC OPERATIONS ====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Historical Candlesticks", f"{stats[0]:,} days")
col2.metric("Average Close Price", f"${stats[1]:,.2f}")
col3.metric("Max High (Period)", f"${stats[2]:,.2f}")
col4.metric("Min Low (Period)", f"${stats[3]:,.2f}")

st.write("---")

latest = load_latest_signal(selected_symbol)
if latest:
    c_price, rsi, macd, sig, sma20, sma50, good_pair, t_stamp, change, vol, fng_val, fng_class, hr, hr_price = latest
    col_sig, col_m1, col_m2, col_m3 = st.columns([1.5, 1, 1, 1])
    with col_sig:
        st.success(f"🟢 **MARKET SENTIMENT: {fng_class} (F&G: {fng_val})**\n\nActive crypto market index suggests stability.")
    with col_m1:
        st.metric("Latest Close", f"${c_price:,.2f}", f"{change:+.2f}% (24h)")
    with col_m2:
        st.metric("Volatility Index", f"{vol:.2f}%")
    with col_m3:
        st.metric("Bitcoin Hash Rate", f"{hr/1e6:.1f}M TH/s" if hr else "unknown")
    st.caption(f"Last updated: {t_stamp}")

st.write("---")

candles_df = load_candles(selected_symbol)
candles_df['date_str'] = candles_df['date'].dt.strftime('%Y-%m-%d')

st.subheader(f"{selected_symbol} Historical Close Price Trend with SMA Overlays")
base = alt.Chart(candles_df).encode(x=alt.X("date_str:N", title="Date (UTC)"))
close_line = base.mark_line(color="#00E5FF", strokeWidth=2).encode(
    y=alt.Y("close_price:Q", title="Price ($)", scale=alt.Scale(zero=False)),
    tooltip=["date_str", "close_price"]
)
sma20_line = base.mark_line(color="#FFD700", strokeDash=[4, 4]).encode(y=alt.Y("sma_20:Q"), tooltip=["date_str", "sma_20"])
sma50_line = base.mark_line(color="#FF4500", strokeDash=[2, 2]).encode(y=alt.Y("sma_50:Q"), tooltip=["date_str", "sma_50"])
st.altair_chart(alt.layer(close_line, sma20_line, sma50_line).properties(height=320), use_container_width=True)

st.write("---")
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("CoinGecko Trending Narratives")
    trending_df = load_trending_narratives()
    if not trending_df.empty:
        trending_chart = alt.Chart(trending_df).mark_arc(innerRadius=40).encode(
            theta=alt.Theta("weight:Q"),
            color=alt.Color("name:N", scale=alt.Scale(scheme="category20")),
            tooltip=["name", "symbol"]
        ).properties(height=260)
        st.altair_chart(trending_chart, use_container_width=True)
    else:
        st.info("No CoinGecko trending narratives found.")

with c2:
    st.subheader("Historical Candlestick & Indicator Ledger")
    st.dataframe(load_ledger(selected_symbol), use_container_width=True)

st.write("---")

# ==================== TIER 2: ACTIONABLE MONETIZATION STRATEGY ====================
st.subheader("Monetization Insights & Ad Copy Generation")

fng_sentiment = fng_class if latest else "Neutral"
btc_price_ref = c_price if latest else 60000.0

st.markdown(f"""
> **Target Audience Profile:** Algorithmic retail investors and high-leverage crypto traders monitoring **{selected_symbol}** changes and global network health indicators.
> **Identified Market Vulnerability:** Cryptocurrency markets demonstrate a **{fng_sentiment}** sentiment profile. Volatility indexes tracking at **{vol:.2f}%** present a prime opportunity to market automated breakout trading tools.

#### Recommended Ad Copy Hooks:
1. **Hook 1 (Emotional Angle):** "Stop trading on fear. When the market is in a **{fng_sentiment}** state, let mathematically backed algorithms handle your execution."
2. **Hook 2 (Data-Driven Angle):** "With {selected_symbol} trading at ${btc_price_ref:,.2f} and volatility tracking at {vol:.2f}%, manual trading can't keep up. Get our custom indicators now."
""")

import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="G-Trend Screener - Binance Market", layout="wide")

st.title("📈 Binance Market Data Analytics")
st.markdown("Historical Bitcoin (BTCUSDT) daily candlestick data, trading volumes, and volatility metrics directly from the public Binance API.")

db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()

conn = duckdb.connect(db_path, read_only=True)

# Fetch general stats
stats = conn.execute("""
    SELECT 
        COUNT(*) as total_candles,
        AVG(close_price) as avg_close,
        MAX(high_price) as max_high,
        MIN(low_price) as min_low
    FROM fact_binance_klines
""").fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Historical Candlesticks", f"{stats[0]:,} days")
col2.metric("Average Close Price", f"${stats[1]:,.2f}")
col3.metric("Max High (Period)", f"${stats[2]:,.2f}")
col4.metric("Min Low (Period)", f"${stats[3]:,.2f}")

st.write("---")

# Fetch and order candles
candles_df = conn.execute("""
    SELECT 
        open_timestamp as date,
        open_price,
        high_price,
        low_price,
        close_price,
        trade_volume
    FROM fact_binance_klines
    ORDER BY open_timestamp ASC
""").df()

# Convert date to string format for display
candles_df['date_str'] = candles_df['date'].dt.strftime('%Y-%m-%d')

st.subheader("BTCUSDT Historical Close Price Trend")
price_chart = alt.Chart(candles_df).mark_line(color="#00E5FF").encode(
    x=alt.X("date_str:N", title="Date (UTC)"),
    y=alt.Y("close_price:Q", title="Close Price ($)", scale=alt.Scale(zero=False)),
    tooltip=["date_str", "open_price", "high_price", "low_price", "close_price"]
).properties(height=350)

st.altair_chart(price_chart, use_container_width=True)

st.write("---")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("BTC Daily Trading Volume Trend")
    volume_chart = alt.Chart(candles_df).mark_bar(color="#7D2AE8").encode(
        x=alt.X("date_str:N", title="Date"),
        y=alt.Y("trade_volume:Q", title="Volume (BTC)"),
        tooltip=["date_str", "trade_volume"]
    ).properties(height=300)
    st.altair_chart(volume_chart, use_container_width=True)

with c2:
    st.subheader("Recent Historical Market Data Ledger")
    # Display the last 100 entries sorted descending
    recent_df = conn.execute("""
        SELECT 
            open_timestamp,
            open_price,
            high_price,
            low_price,
            close_price,
            trade_volume,
            total_trades
        FROM fact_binance_klines
        ORDER BY open_timestamp DESC
        LIMIT 100
    """).df()
    st.dataframe(recent_df, use_container_width=True)

conn.close()

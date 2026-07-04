import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="G-Trend Screener - Binance Market", layout="wide")

st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 30, 40, 0.8), rgba(20, 20, 30, 0.9));
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: transform 0.2s;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(228, 255, 0, 0.4);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #B2B2B2;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chart-container {
        background: rgba(20, 20, 30, 0.6);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header("📊 Market Selector")
selected_symbol = st.sidebar.selectbox("Select Asset Pair", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

st.markdown(f"<h1 style='font-weight: 900; background: linear-gradient(90deg, #FFD700, #FF8C00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{selected_symbol} Quantitative Screener</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #B2B2B2;'>Real-time cryptocurrency analytics, technical indicators, and sentiment prediction algorithms.</p>", unsafe_allow_html=True)

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("Production database not found. Please run the ETL pipeline.")
    st.stop()

@st.cache_data
def load_latest_signal(symbol):
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute(f"SELECT close_price, rsi_14, macd_line, sma_20, fng_value, fng_classification, btc_hash_rate, volatility_index FROM fact_binance_klines WHERE symbol = '{symbol}' ORDER BY open_timestamp DESC LIMIT 1").fetchone()
    conn.close()
    return result

@st.cache_data
def load_candles(symbol):
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute(f"SELECT open_timestamp as date, close_price, rsi_14, sma_20, sma_50, trade_volume FROM fact_binance_klines WHERE symbol = '{symbol}' ORDER BY open_timestamp ASC").df()
    conn.close()
    return df

@st.cache_data
def load_trending_narratives():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT trending_coin_name as name, trending_coin_symbol as symbol, 1.0 AS weight FROM fact_binance_klines").df()
    conn.close()
    return df.drop_duplicates(subset=["name"])

latest = load_latest_signal(selected_symbol)
c_price, rsi, macd, sma20, fng_val, fng_class, hr, vol = latest if latest else (0,0,0,0,0,"N/A",0,0)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Latest Price</div><div class='metric-val'>${c_price:,.2f}</div><div style='color: #00FF66; font-size: 0.85rem;'>Live Data</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>RSI (14)</div><div class='metric-val'>{rsi:.1f}</div><div style='color: #FFB300; font-size: 0.85rem;'>Momentum</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Sentiment Score</div><div class='metric-val'>{fng_val}</div><div style='color: #FF4500; font-size: 0.85rem;'>{fng_class}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Volatility</div><div class='metric-val'>{vol:.2f}%</div><div style='color: #00E5FF; font-size: 0.85rem;'>Risk Metric</div></div>", unsafe_allow_html=True)

candles_df = load_candles(selected_symbol)
candles_df['date_str'] = candles_df['date'].dt.strftime('%Y-%m-%d')

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown(f"<div class='chart-container'><h3>📈 {selected_symbol} Predictive Moving Averages</h3></div>", unsafe_allow_html=True)
    base = alt.Chart(candles_df).encode(x=alt.X("date_str:N", title="Date (UTC)"))
    close_line = base.mark_line(color="#FFD700", strokeWidth=3).encode(y=alt.Y("close_price:Q", title="Price ($)", scale=alt.Scale(zero=False)))
    sma20_line = base.mark_line(color="#00E5FF", strokeDash=[4, 4]).encode(y=alt.Y("sma_20:Q"))
    sma50_line = base.mark_line(color="#FF4500", strokeDash=[2, 2]).encode(y=alt.Y("sma_50:Q"))
    st.altair_chart(alt.layer(close_line, sma20_line, sma50_line).properties(height=350), use_container_width=True)

with c2:
    st.markdown("<div class='chart-container'><h3>🔥 RSI Oscillation Engine</h3></div>", unsafe_allow_html=True)
    rsi_chart = alt.Chart(candles_df).mark_area(opacity=0.3, color="#FF00E5").encode(
        x=alt.X("date_str:N", title="Date"),
        y=alt.Y("rsi_14:Q", title="RSI", scale=alt.Scale(domain=[0, 100])),
        tooltip=["date_str", "rsi_14"]
    ).properties(height=350)
    st.altair_chart(rsi_chart, use_container_width=True)

st.write("---")
c3, c4 = st.columns([1, 1])
with c3:
    st.markdown("<div class='chart-container'><h3>🔍 On-Chain Network Hash Rate Analysis</h3></div>", unsafe_allow_html=True)
    conn = duckdb.connect(DB_PATH, read_only=True)
    hr_df = conn.execute("SELECT open_timestamp::DATE as date, AVG(btc_hash_rate) as hr FROM fact_binance_klines WHERE btc_hash_rate IS NOT NULL GROUP BY date ORDER BY date").df()
    conn.close()
    if not hr_df.empty:
        hr_df['date_str'] = pd.to_datetime(hr_df['date']).dt.strftime('%Y-%m-%d')
        hr_chart = alt.Chart(hr_df).mark_bar(color="#FF8C00").encode(
            x=alt.X("date_str:N", title="Date"),
            y=alt.Y("hr:Q", title="Hash Rate"),
            tooltip=["date_str", "hr"]
        ).properties(height=300)
        st.altair_chart(hr_chart, use_container_width=True)

with c4:
    st.markdown("<div class='chart-container'><h3>🧬 Altcoin Narrative Weighting</h3></div>", unsafe_allow_html=True)
    trending_df = load_trending_narratives()
    if not trending_df.empty:
        trending_chart = alt.Chart(trending_df).mark_arc(innerRadius=60).encode(
            theta=alt.Theta("weight:Q"),
            color=alt.Color("name:N", scale=alt.Scale(scheme="category10")),
            tooltip=["name", "symbol"]
        ).properties(height=300)
        st.altair_chart(trending_chart, use_container_width=True)

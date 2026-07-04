import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="G-Trend screener Quantitative Analytics", layout="wide")

st.title("📈 G-Trend quantitative Strategy Screener")
st.markdown("Quantitative trading metrics, win-rate distributions, and peak-to-trough risk profiling from TradingView strategy logs.")

db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()

conn = duckdb.connect(db_path, read_only=True)

# Query Trade Stats
stats = conn.execute("""
    SELECT 
        COUNT(*) as total_trades,
        AVG(profit_loss_percentage) as avg_pl,
        SUM(profit_loss_percentage) as cumulative_return,
        MAX(max_drawdown_percentage) as peak_drawdown,
        COUNT(*) FILTER (WHERE profit_loss_percentage > 0) * 100.0 / COUNT(*) as win_rate,
        COALESCE(
            SUM(profit_loss_percentage) FILTER (WHERE profit_loss_percentage > 0) / 
            ABS(SUM(profit_loss_percentage) FILTER (WHERE profit_loss_percentage <= 0)), 
            1.0
        ) as profit_factor
    FROM fact_gtrend_trades
""").fetchone()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Trades", f"{stats[0]:,}")
col2.metric("Cumulative P&L", f"{stats[2]:+.2f}%")
col3.metric("Trade Win Rate", f"{stats[4]:.2f}%")
col4.metric("Profit Factor", f"{stats[5]:.2f}x")
col5.metric("Max Peak Drawdown", f"{stats[3]:.2f}%", delta_color="inverse")

st.write("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Asset Pair Profitability Breakdown")
    asset_pl = conn.execute("""
        SELECT 
            asset_pair, 
            AVG(profit_loss_percentage) as avg_pl,
            COUNT(*) as trades_count
        FROM fact_gtrend_trades
        GROUP BY 1
        ORDER BY avg_pl DESC
    """).df()
    
    asset_chart = alt.Chart(asset_pl).mark_bar().encode(
        x=alt.X("avg_pl:Q", title="Average Return (%)"),
        y=alt.Y("asset_pair:N", sort="-x", title="Asset"),
        color=alt.condition(
            alt.datum.avg_pl > 0,
            alt.value("#00E5FF"), # positive Cyan
            alt.value("#FF3333")  # negative Red
        ),
        tooltip=["asset_pair", "avg_pl", "trades_count"]
    ).properties(height=300)
    st.altair_chart(asset_chart, use_container_width=True)

with c2:
    st.subheader("P&L Distribution by Trade Position Type")
    pos_df = conn.execute("""
        SELECT 
            position_type,
            COUNT(*) as count,
            AVG(profit_loss_percentage) as avg_pl
        FROM fact_gtrend_trades
        GROUP BY 1
    """).df()
    
    pos_chart = alt.Chart(pos_df).mark_bar(color="#7D2AE8").encode(
        x=alt.X("position_type:N", title="Position Type"),
        y=alt.Y("count:Q", title="Number of Trades"),
        color=alt.Color("position_type:N", scale=alt.Scale(scheme="purples")),
        tooltip=["position_type", "count", "avg_pl"]
    ).properties(height=300)
    st.altair_chart(pos_chart, use_container_width=True)

st.write("---")

st.subheader("Historical quantitative Trade Ledger")
ledger_df = conn.execute("""
    SELECT 
        trade_id,
        asset_pair,
        entry_timestamp,
        exit_timestamp,
        position_type,
        profit_loss_percentage as profit_loss,
        max_drawdown_percentage as max_drawdown,
        duration_hours
    FROM fact_gtrend_trades
    ORDER BY entry_timestamp DESC
    LIMIT 100
""").df()

st.dataframe(ledger_df, use_container_width=True)

conn.close()

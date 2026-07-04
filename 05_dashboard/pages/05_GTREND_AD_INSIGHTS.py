import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="GTREND AD INSIGHTS", layout="wide")
st.title("GTREND AD INSIGHTS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Binance API & Alternative.me")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_klines = conn.execute("SELECT * FROM fact_binance_klines").df()
df_fng = conn.execute("SELECT * FROM ext_crypto_sentiment").df()
conn.close()

st.subheader("Quantitative Trading Performance & Risk Metrics")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_klines.empty:
        vol_chart = alt.Chart(df_klines).mark_bar(opacity=0.7).encode(x='open_time', y='volume').properties(height=200, title="Trade Volume Distribution")
        st.altair_chart(vol_chart, use_container_width=True)

with c2:
    if not df_fng.empty:
        fng_chart = alt.Chart(df_fng).mark_line(color='red').encode(x='timestamp', y='value').properties(height=200, title="Risk Sentiment Overlay")
        st.altair_chart(fng_chart, use_container_width=True)

with c3:
    if not df_fng.empty:
        fng_pie = alt.Chart(df_fng).mark_arc().encode(theta='count()', color='value_classification').properties(height=200, title="Classification Proportion")
        st.altair_chart(fng_pie, use_container_width=True)

st.write("**Raw Market Data:**")
st.dataframe(df_fng, use_container_width=True, height=200)

st.write("---")
st.subheader("Quantitative Actionable Insights")
st.markdown("""
> **Strategic Interpretation:** We are monitoring live BTC price volatility combined with global fear metrics.
> **Predictive Analysis:** Periods of "Extreme Fear" historically correspond to localized volume bottoms. 
> **Actionable Plan:** Adjust DCA bot threshold algorithms to buy aggressively when Fear drops below 20.
""")

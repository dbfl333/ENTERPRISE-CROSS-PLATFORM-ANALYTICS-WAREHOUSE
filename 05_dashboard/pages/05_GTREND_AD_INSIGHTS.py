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
df = conn.execute("SELECT symbol, fng_classification, COUNT(*) as count FROM fact_binance_klines GROUP BY symbol, fng_classification").df()
conn.close()

st.subheader("Crypto Narrative Targeting")
if not df.empty:
    c = alt.Chart(df).mark_bar().encode(x='fng_classification', y='count', color='symbol').properties(height=250, title="Sentiment Classification Distribution")
    st.altair_chart(c, use_container_width=True)

st.write("---")
st.subheader("Revenue Generation Suggestions")
st.markdown("""
> **Strategic Interpretation:** Real-time sentiment metrics (Fear & Greed) heavily influence crypto-native purchasing behavior.
> **Target Audience Prediction:** When the market shifts into 'Extreme Fear', we should target retail traders with 'Risk Mitigation' and 'Safe Haven' algorithmic tools. 
> **Actionable Plan:** Dynamically adjust our ad copy using an API webhook that changes the Facebook Ads messaging based on the live `fng_classification` row data.
""")

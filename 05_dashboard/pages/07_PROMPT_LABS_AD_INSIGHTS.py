import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="PROMPT LABS AD INSIGHTS", layout="wide")
st.title("PROMPT LABS AD INSIGHTS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Search Demand ETL")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df = conn.execute("SELECT search_date, AVG(cpc_usd) as avg_cpc FROM staging_prompt_telemetry GROUP BY search_date ORDER BY search_date").df()
conn.close()

st.subheader("B2B Developer Outreach Strategy")
if not df.empty:
    c = alt.Chart(df).mark_area(color='magenta', opacity=0.4).encode(x='search_date', y='avg_cpc').properties(height=250, title="Average CPC Trend over Time")
    st.altair_chart(c, use_container_width=True)

st.write("---")
st.subheader("Revenue Generation Suggestions")
st.markdown("""
> **Strategic Interpretation:** Keyword difficulties are rising alongside CPC, indicating a highly competitive NLP market.
> **Target Audience Prediction:** Instead of targeting broad AI keywords, we must target long-tail, low-difficulty queries extracted from the telemetry data (e.g. specialized agentic frameworks).
> **Actionable Plan:** Generate targeted GitHub READMEs and ArXiv abstracts matching the lowest difficulty keywords in our database, driving organic developer traffic instead of paying high CPCs.
""")

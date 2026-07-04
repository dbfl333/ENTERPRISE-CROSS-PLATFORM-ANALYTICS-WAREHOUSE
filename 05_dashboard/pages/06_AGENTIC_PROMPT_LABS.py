import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AGENTIC PROMPT LABS", layout="wide")
st.title("AGENTIC PROMPT LABS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: GitHub API & ArXiv")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
conn.close()

st.subheader("Prompt Engineering Telemetry")
c1, c2 = st.columns(2)

with c1:
    if not df.empty:
        cpc_chart = alt.Chart(df).mark_point(filled=True, size=60).encode(x='keyword_difficulty', y='cpc_usd', color='search_interest_score', tooltip=['keyword']).properties(height=250, title="Difficulty vs CPC Scatter")
        st.altair_chart(cpc_chart, use_container_width=True)

with c2:
    if not df.empty:
        hist_chart = alt.Chart(df).mark_bar().encode(alt.X('search_interest_score', bin=True), y='count()').properties(height=250, title="Search Interest Distribution")
        st.altair_chart(hist_chart, use_container_width=True)

st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Prompt Labs Telemetry SQL"):
    st.dataframe(df, use_container_width=True)

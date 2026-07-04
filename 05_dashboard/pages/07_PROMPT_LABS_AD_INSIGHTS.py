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
    st.caption("Source: Telemetry SEO Engine & Google Trends")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_telemetry = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
df_trends = conn.execute("SELECT * FROM ext_prompt_google_trends").df()
conn.close()

st.subheader("SaaS Cost per Acquisition Analysis")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_telemetry.empty:
        cpc_chart = alt.Chart(df_telemetry).mark_bar(color='green').encode(x='keyword_tracked', y='estimated_cpc_high').properties(height=180, title="CPC Cost per Keyword")
        st.altair_chart(cpc_chart, use_container_width=True)

with c2:
    if not df_trends.empty:
        diff_chart = alt.Chart(df_trends).mark_line().encode(x='search_date:T', y='search_interest_score', color='keyword_tracked').properties(height=180, title="Google Trends Overlay")
        st.altair_chart(diff_chart, use_container_width=True)

with c3:
    if not df_telemetry.empty:
        scatter = alt.Chart(df_telemetry).mark_point(filled=True).encode(x='search_interest_score', y='estimated_cpc_high', color='profitable_niche_flag').properties(height=180, title="Cost vs Interest")
        st.altair_chart(scatter, use_container_width=True)

st.write("**Raw SEO & Search Trends:**")
st.dataframe(df_trends, use_container_width=True, height=150)

st.write("---")
st.subheader("B2B Marketing Strategy")
st.markdown("""
> **Strategic Interpretation:** B2B developer terms are notoriously expensive. High CPC with Low Search Interest means we are overpaying.
> **Actionable Plan:** Pause all Google Ads for "profitable_niche_flag = False" keywords. Redirect that budget into HackerNews content sponsorship.
""")

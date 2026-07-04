import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AGENTIC PROMPT LABS", layout="wide")
st.title("AGENTIC PROMPT LABS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync3"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: SEO Telemetry ---
st.write("---")
st.subheader("Source 1: CPC & SEO Telemetry")
st.markdown("> **Strategic Value:** Understanding the cost barrier to acquiring B2B developers via paid ads.")
df_telemetry = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
if not df_telemetry.empty:
    c1, c2 = st.columns(2)
    with c1:
        # BUG FIX: Removed 'keyword' from tooltip to fix ValueError
        c = alt.Chart(df_telemetry).mark_point(filled=True, size=60).encode(x='organic_difficulty', y='estimated_cpc_high', color='search_interest_score').properties(height=200, title="Difficulty vs CPC Scatter")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_telemetry).mark_bar().encode(alt.X('search_interest_score', bin=True), y='count()').properties(height=200, title="Search Interest Distribution")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: GitHub Demand ---
st.write("---")
st.subheader("Source 2: GitHub Repository Demand")
st.markdown("> **Strategic Value:** Identifying which open-source AI repos are getting the most stars and forks.")
df_gh = conn.execute("SELECT * FROM ext_github_agent_demand").df()
if not df_gh.empty:
    c = alt.Chart(df_gh).mark_bar(color='gray').encode(x='name', y='stargazers_count', color='forks_count').properties(height=200, title="Top Repo Stargazers")
    st.altair_chart(c, use_container_width=True)

# --- Source 3: HackerNews ---
st.write("---")
st.subheader("Source 3: Tech Ecosystem Sentiment (HackerNews)")
st.markdown("> **Strategic Value:** Gauging velocity of developer discourse around AI agents.")
df_hn = conn.execute("SELECT * FROM ext_hackernews_tech").df()
if not df_hn.empty:
    st.write(f"Total Top Stories Pulled: {len(df_hn)}")
    st.dataframe(df_hn, use_container_width=True)

# --- Source 4: ArXiv Research ---
st.write("---")
st.subheader("Source 4: Academic Horizon (ArXiv)")
st.markdown("> **Strategic Value:** Projecting what agentic frameworks will hit the commercial market in 6-12 months.")
df_arxiv = conn.execute("SELECT * FROM ext_arxiv_trends").df()
if not df_arxiv.empty:
    c = alt.Chart(df_arxiv).mark_point().encode(x='published', y='title').properties(height=200, title="Recent Paper Publications")
    st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Telemetry"); st.dataframe(df_telemetry, use_container_width=True)
    st.write("GitHub Demand"); st.dataframe(df_gh, use_container_width=True)
    st.write("ArXiv Papers"); st.dataframe(df_arxiv, use_container_width=True)
conn.close()

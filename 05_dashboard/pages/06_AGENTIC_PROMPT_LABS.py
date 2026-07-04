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
df_telemetry = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
df_gh = conn.execute("SELECT * FROM ext_github_agent_demand").df()
df_hn = conn.execute("SELECT * FROM ext_hackernews_tech").df()
df_arxiv = conn.execute("SELECT * FROM ext_arxiv_trends").df()
conn.close()

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: SEO Telemetry ---
st.write("---")
st.subheader("Source 1: CPC & SEO Telemetry")
st.markdown("> **Strategic Value:** Understanding the cost barrier to acquiring B2B developers via paid ads.")
c1, c2, c3 = st.columns(3)
if not df_telemetry.empty:
    with c1:
        c = alt.Chart(df_telemetry).mark_point(filled=True, size=60).encode(x='organic_difficulty', y='estimated_cpc_high', color='search_interest_score').properties(height=180, title="Difficulty vs CPC Scatter")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_telemetry).mark_bar().encode(alt.X('search_interest_score', bin=True), y='count()').properties(height=180, title="Interest Distribution")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_telemetry).mark_arc().encode(theta='count()', color='competition_level').properties(height=180, title="Competition Landscape")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_telemetry, use_container_width=True, height=150)

# --- Source 2: GitHub Demand ---
st.write("---")
st.subheader("Source 2: GitHub Repository Demand")
st.markdown("> **Strategic Value:** Identifying which open-source AI repos are getting the most stars and forks.")
c1, c2 = st.columns(2)
if not df_gh.empty:
    with c1:
        c = alt.Chart(df_gh).mark_bar(color='gray').encode(x='name', y='stargazers_count', color='forks_count').properties(height=180, title="Top Repo Stargazers")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_gh).mark_point(color='green').encode(x='stargazers_count', y='forks_count').properties(height=180, title="Stars vs Forks Matrix")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_gh, use_container_width=True, height=150)

# --- Source 3: HackerNews ---
st.write("---")
st.subheader("Source 3: Tech Ecosystem Sentiment (HackerNews)")
st.markdown("> **Strategic Value:** Gauging velocity of developer discourse around AI agents.")
c1, c2 = st.columns(2)
if not df_hn.empty:
    with c1:
        c = alt.Chart(df_hn).mark_bar().encode(x='story_id', y='count()').properties(height=180, title="Story Ingestion Count")
        st.altair_chart(c, use_container_width=True)
    with c2:
        st.metric("Total Stories Scraped", len(df_hn))
st.write("**Raw Source Data:**")
st.dataframe(df_hn, use_container_width=True, height=150)

# --- Source 4: ArXiv Research ---
st.write("---")
st.subheader("Source 4: Academic Horizon (ArXiv)")
st.markdown("> **Strategic Value:** Projecting what agentic frameworks will hit the commercial market in 6-12 months.")
c1, c2 = st.columns(2)
if not df_arxiv.empty:
    with c1:
        c = alt.Chart(df_arxiv).mark_point(color='red').encode(x='published', y='title').properties(height=180, title="Recent Papers")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_arxiv).mark_bar(color='purple').encode(x='published', y='count()').properties(height=180, title="Publication Velocity")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_arxiv, use_container_width=True, height=150)

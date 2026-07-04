import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Prompt Labs Market Demand - Analytics Warehouse", layout="wide")

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
        border-color: rgba(0, 255, 102, 0.4);
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
        background: linear-gradient(90deg, #00FF66, #00E5FF);
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

st.markdown("<h1 style='font-weight: 900; background: linear-gradient(90deg, #00FF66, #00E5FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Agentic Prompt Labs Telemetry</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #B2B2B2;'>Predictive search interest modeling, CPC forecasting, and organic difficulty clustering for NLP and AI agent markets.</p>", unsafe_allow_html=True)

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("Production database not found. Please run the ETL pipeline.")
    st.stop()

@st.cache_data
def load_keyword_stats():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT keyword_tracked as keyword, AVG(search_interest_score) as avg_interest,
               AVG(organic_difficulty) as avg_difficulty, AVG(estimated_cpc_high) as avg_cpc_high,
               COUNT(CASE WHEN profitable_niche_flag THEN 1 END) as profitable_weeks
        FROM staging_prompt_telemetry GROUP BY 1
    """).df()
    conn.close()
    return df

@st.cache_data
def load_trends_timeline():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT search_date as date, keyword_tracked as keyword, search_interest_score FROM staging_prompt_telemetry ORDER BY search_date ASC").df()
    conn.close()
    return df

@st.cache_data
def load_github_shares():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT DISTINCT top_github_repo as name, top_github_stars as stars FROM staging_prompt_telemetry").df()
    conn.close()
    return df

kw_stats = load_keyword_stats()
avg_cpc = kw_stats['avg_cpc_high'].mean() if not kw_stats.empty else 0.0
avg_diff = kw_stats['avg_difficulty'].mean() if not kw_stats.empty else 0.0
prof_weeks = kw_stats['profitable_weeks'].sum() if not kw_stats.empty else 0
total_kws = len(kw_stats)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Keywords Tracked</div><div class='metric-val'>{total_kws}</div><div style='color: #00E5FF; font-size: 0.85rem;'>Agentic AI Focus</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Average CPC (High)</div><div class='metric-val'>${avg_cpc:.2f}</div><div style='color: #FFB300; font-size: 0.85rem;'>Target ROI Base</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Organic Difficulty</div><div class='metric-val'>{avg_diff:.1f}</div><div style='color: #FF4500; font-size: 0.85rem;'>SEO Threshold</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Profitable Weeks</div><div class='metric-val'>{prof_weeks}</div><div style='color: #00FF66; font-size: 0.85rem;'>Niche Viability</div></div>", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("<div class='chart-container'><h3>📈 Predictive Search Demand Timeline</h3></div>", unsafe_allow_html=True)
    trends_df = load_trends_timeline()
    trends_df['date_str'] = pd.to_datetime(trends_df['date']).dt.strftime('%Y-%m-%d')
    chart = alt.Chart(trends_df).mark_line(strokeWidth=3, interpolate='monotone').encode(
        x=alt.X("date_str:N", title="Search Date"),
        y=alt.Y("search_interest_score:Q", title="Interest Score (0-100)"),
        color=alt.Color("keyword:N", title="Keyword", scale=alt.Scale(scheme="set1")),
        tooltip=["date_str", "keyword", "search_interest_score"]
    ).properties(height=250)
    st.altair_chart(chart, use_container_width=True)

with c2:
    st.markdown("<div class='chart-container'><h3>🧩 Open Source Repository Gravity</h3></div>", unsafe_allow_html=True)
    git_shares_df = load_github_shares()
    if not git_shares_df.empty:
        git_chart = alt.Chart(git_shares_df).mark_arc(innerRadius=60).encode(
            theta=alt.Theta("stars:Q"),
            color=alt.Color("name:N", scale=alt.Scale(scheme="dark2")),
            tooltip=["name", "stars"]
        ).properties(height=250)
        st.altair_chart(git_chart, use_container_width=True)

st.write("---")

c3, c4 = st.columns([1, 1])
with c3:
    st.markdown("<div class='chart-container'><h3>📊 Keyword CPC vs Organic Difficulty Cluster</h3></div>", unsafe_allow_html=True)
    if not kw_stats.empty:
        scatter = alt.Chart(kw_stats).mark_circle(size=300, opacity=0.8).encode(
            x=alt.X('avg_difficulty:Q', title='Organic Difficulty'),
            y=alt.Y('avg_cpc_high:Q', title='Estimated CPC High ($)'),
            color=alt.Color('keyword:N', scale=alt.Scale(scheme='spectral')),
            size=alt.Size('avg_interest:Q', title='Search Interest', scale=alt.Scale(range=[100, 1000])),
            tooltip=['keyword', 'avg_difficulty', 'avg_cpc_high', 'avg_interest']
        ).properties(height=250)
        st.altair_chart(scatter, use_container_width=True)

with c4:
    st.markdown("<div class='chart-container'><h3>💡 Market Momentum & Competition Density</h3></div>", unsafe_allow_html=True)
    conn = duckdb.connect(DB_PATH, read_only=True)
    mom_df = conn.execute("SELECT keyword_tracked as keyword, AVG(weekly_momentum_pct) as momentum, MAX(competition_level) as competition FROM staging_prompt_telemetry GROUP BY keyword").df()
    conn.close()
    if not mom_df.empty:
        mom_chart = alt.Chart(mom_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('keyword:N', title='Keyword', sort='-y'),
            y=alt.Y('momentum:Q', title='Weekly Momentum (%)'),
            color=alt.Color('competition:N', scale=alt.Scale(scheme='category20')),
            tooltip=['keyword', 'momentum', 'competition']
        ).properties(height=250)
        st.altair_chart(mom_chart, use_container_width=True)

st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Prompt Labs Telemetry SQL"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.dataframe(conn.execute("SELECT * FROM staging_prompt_telemetry ORDER BY search_date DESC LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** We are identifying profitable niches where search interest is climbing while organic SEO difficulty remains manageable.
> **Target Audience Prediction:** Target AI product managers and backend developers searching for 'Agentic AI' templates. High GitHub star gravity indicates a strong demand for open-source foundation models.
> **Actionable Plan:** Produce high-technical-depth content (whitepapers, ArXiv summaries) targeting the exact keywords where CPC is high but organic difficulty is low, capturing enterprise B2B leads.
""")

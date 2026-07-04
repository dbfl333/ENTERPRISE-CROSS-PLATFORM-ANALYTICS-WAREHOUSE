import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import os

st.set_page_config(
    page_title="Enterprise Multi-AI Markets Shop Analytics",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 30, 40, 0.8), rgba(20, 20, 30, 0.9));
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: transform 0.3s, border-color 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 224, 255, 0.6);
    }
    .main-header {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00E5FF, #FF00E5, #7D2AE8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-text {
        color: #C0C0C0;
        font-size: 1.2rem;
        margin-bottom: 30px;
        font-weight: 300;
        max-width: 900px;
    }
    .chart-container {
        background: rgba(20, 20, 30, 0.6);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Multi-AI Markets Shop Administration & Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Target potential clients using predictive analytics. We gather multi-source telemetry so we can see <b>who</b>, <b>where</b>, <b>when</b>, and <b>why</b> we can target users. Our data science pipelines feed rich predictive models across 5 core projects.</p>", unsafe_allow_html=True)

DB_PATH = "04_clean_data/analytics_production.duckdb"

if not os.path.exists(DB_PATH):
    st.error("Production database not found. Please run the ETL pipeline.")
    st.stop()

@st.cache_data
def load_overview_data():
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    # 1. Shop Orders Geo
    geo_df = conn.execute("SELECT geo_country, COUNT(*) as orders, SUM(total_amount) as revenue FROM fact_shop_orders WHERE geo_country IS NOT NULL GROUP BY geo_country ORDER BY revenue DESC").df()
    
    # 2. GA4 Session Sources
    traffic_df = conn.execute("SELECT session_source, SUM(sessions) as sessions, SUM(total_revenue) as revenue FROM staging_ga4_sessions GROUP BY session_source ORDER BY sessions DESC LIMIT 5").df()
    
    # 3. Marketing ROI
    marketing_df = conn.execute("SELECT channel, SUM(spend) as spend, SUM(attributed_revenue) as revenue FROM staging_shopify_marketing GROUP BY channel").df()
    
    # 4. Crypto Sentiment (Binance)
    crypto_df = conn.execute("SELECT open_timestamp::DATE as date, AVG(close_price) as avg_price, AVG(fng_value) as fng FROM fact_binance_klines GROUP BY date ORDER BY date").df()
    
    # 5. Terrazas Bookings by Event Type
    terrazas_df = conn.execute("SELECT event_type, COUNT(*) as bookings, SUM(total_gross_amount) as revenue FROM staging_terrazas_bookings GROUP BY event_type").df()

    conn.close()
    return geo_df, traffic_df, marketing_df, crypto_df, terrazas_df

geo_df, traffic_df, marketing_df, crypto_df, terrazas_df = load_overview_data()

# KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <h4 style="color:#B2B2B2; margin:0;">Global Reach</h4>
        <h2 style="color:#00E5FF; margin:0;">{len(geo_df)} Countries</h2>
        <p style="color:#00FF66; margin:0;">Active predictive targeting</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4 style="color:#B2B2B2; margin:0;">Total Traffic</h4>
        <h2 style="color:#FF00E5; margin:0;">{int(traffic_df['sessions'].sum()):,}</h2>
        <p style="color:#00FF66; margin:0;">Qualified prospect sessions</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4 style="color:#B2B2B2; margin:0;">Marketing ROI</h4>
        <h2 style="color:#7D2AE8; margin:0;">${marketing_df['revenue'].sum():,.2f}</h2>
        <p style="color:#00FF66; margin:0;">Attributed channel revenue</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4 style="color:#B2B2B2; margin:0;">Venue Bookings</h4>
        <h2 style="color:#FFB300; margin:0;">{int(terrazas_df['bookings'].sum())} Events</h2>
        <p style="color:#00FF66; margin:0;">High-value engagements</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Charts Row 1
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='chart-container'><h3>🌍 User Acquisition by Channel (Predictive Weights)</h3></div>", unsafe_allow_html=True)
    pie_chart = alt.Chart(traffic_df).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="sessions", type="quantitative"),
        color=alt.Color(field="session_source", type="nominal", scale=alt.Scale(scheme="category20c")),
        tooltip=["session_source", "sessions", "revenue"]
    ).properties(height=350)
    st.altair_chart(pie_chart, use_container_width=True)

with c2:
    st.markdown("<div class='chart-container'><h3>🎯 Event Type Segmentation (Terrazas)</h3></div>", unsafe_allow_html=True)
    bar_chart = alt.Chart(terrazas_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X('event_type:N', title='Event Type', sort='-y'),
        y=alt.Y('revenue:Q', title='Revenue ($)'),
        color=alt.Color('event_type:N', scale=alt.Scale(scheme='turbo'), legend=None),
        tooltip=['event_type', 'bookings', 'revenue']
    ).properties(height=350)
    st.altair_chart(bar_chart, use_container_width=True)

st.write("---")

# Charts Row 2
c3, c4 = st.columns(2)

with c3:
    st.markdown("<div class='chart-container'><h3>📈 Crypto Market Sentiment vs Price Action</h3></div>", unsafe_allow_html=True)
    base = alt.Chart(crypto_df).encode(x=alt.X('date:T', title='Timeline'))
    line1 = base.mark_line(color='#00E5FF', strokeWidth=3).encode(y=alt.Y('avg_price:Q', title='BTC Price', scale=alt.Scale(zero=False)))
    line2 = base.mark_line(color='#FF00E5', strokeWidth=2).encode(y=alt.Y('fng:Q', title='Fear & Greed Index'))
    st.altair_chart(alt.layer(line1, line2).resolve_scale(y='independent').properties(height=300), use_container_width=True)

with c4:
    st.markdown("<div class='chart-container'><h3>💰 Marketing Channel ROI Comparison</h3></div>", unsafe_allow_html=True)
    roi_melt = marketing_df.melt(id_vars=['channel'], value_vars=['spend', 'revenue'], var_name='Metric', value_name='Amount')
    roi_chart = alt.Chart(roi_melt).mark_bar().encode(
        x=alt.X('channel:N', title='Marketing Channel'),
        y=alt.Y('Amount:Q', title='USD ($)'),
        color=alt.Color('Metric:N', scale=alt.Scale(range=['#FF4B4B', '#00FF66'])),
        xOffset='Metric:N',
        tooltip=['channel', 'Metric', 'Amount']
    ).properties(height=300)
    st.altair_chart(roi_chart, use_container_width=True)

st.markdown("""
<div style="text-align: center; margin-top: 40px; color: #666;">
    <p><i>Data Engineering Portfolio • Predictive Analytics & Machine Learning Ready Architecture</i></p>
</div>
""", unsafe_allow_html=True)

st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Raw Fact & Staging Tables"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.write("**fact_shop_orders**")
    st.dataframe(conn.execute("SELECT * FROM fact_shop_orders LIMIT 100").df(), use_container_width=True)
    st.write("**staging_ga4_sessions**")
    st.dataframe(conn.execute("SELECT * FROM staging_ga4_sessions LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** The multi-tenant data indicates strong cross-pollination opportunities between high-value E-Commerce clients and algorithmic trading tool adopters.
> **Target Audience Prediction:** We should target users located in regions with high Terrazas event bookings and overlapping GA4 session traffic. These users exhibit high discretionary capital and digital engagement.
> **Actionable Plan:** Deploy ad campaigns focusing on automated revenue generation, targeting the top 3 geographic locations highlighted in our global reach metrics.
""")

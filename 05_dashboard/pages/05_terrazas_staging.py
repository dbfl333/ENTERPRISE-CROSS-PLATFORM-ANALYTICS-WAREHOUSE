import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Terrazas-home - Analytics Warehouse", layout="wide")

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
        border-color: rgba(255, 179, 0, 0.4);
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
        background: linear-gradient(90deg, #FFB300, #FF00E5);
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

st.markdown("<h1 style='font-weight: 900; background: linear-gradient(90deg, #FFB300, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Terrazas-Home Venue Administration</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #B2B2B2;'>Dynamic event pricing matrices, physical inventory telemetry, forecasting multipliers, and lead time algorithmic modeling.</p>", unsafe_allow_html=True)

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("Production database not found. Please run the ETL pipeline.")
    st.stop()

@st.cache_data
def load_kpis():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT COUNT(*) as bookings, SUM(total_gross_amount) as revenue, AVG(lead_time_days) as lead_time, AVG(customer_rating_score) as rating FROM staging_terrazas_bookings").df()
    conn.close()
    return df.iloc[0]

@st.cache_data
def load_event_revenue():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT event_type, COUNT(*) as bookings, SUM(total_gross_amount) as revenue, AVG(seasonal_multiplier) as multiplier FROM staging_terrazas_bookings GROUP BY event_type ORDER BY revenue DESC").df()
    conn.close()
    return df

@st.cache_data
def load_lead_time_distribution():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT event_type, AVG(lead_time_days) as avg_lead_time, MAX(lead_time_days) as max_lead, MIN(lead_time_days) as min_lead FROM staging_terrazas_bookings GROUP BY event_type").df()
    conn.close()
    return df

@st.cache_data
def load_timeline():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT check_in_timestamp::DATE as date, SUM(total_gross_amount) as daily_revenue FROM staging_terrazas_bookings GROUP BY date ORDER BY date").df()
    conn.close()
    return df

kpis = load_kpis()
bookings = int(kpis['bookings']) if not pd.isna(kpis['bookings']) else 0
revenue = float(kpis['revenue']) if not pd.isna(kpis['revenue']) else 0.0
lead = float(kpis['lead_time']) if not pd.isna(kpis['lead_time']) else 0.0
rating = float(kpis['rating']) if not pd.isna(kpis['rating']) else 0.0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Event Volume</div><div class='metric-val'>{bookings}</div><div style='color: #00FF66; font-size: 0.85rem;'>Total Bookings</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Gross Revenue</div><div class='metric-val'>${revenue:,.2f}</div><div style='color: #FFB300; font-size: 0.85rem;'>Staged Capital</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Avg Lead Time</div><div class='metric-val'>{lead:.1f}</div><div style='color: #00E5FF; font-size: 0.85rem;'>Days in Advance</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Customer Rating</div><div class='metric-val'>{rating:.1f}/100</div><div style='color: #FF00E5; font-size: 0.85rem;'>Satisfaction Index</div></div>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("<div class='chart-container'><h3>📅 Predictive Revenue Timeline</h3></div>", unsafe_allow_html=True)
    tl_df = load_timeline()
    if not tl_df.empty:
        tl_df['date_str'] = pd.to_datetime(tl_df['date']).dt.strftime('%Y-%m-%d')
        tl_chart = alt.Chart(tl_df).mark_area(
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#FF00E5', offset=0), alt.GradientStop(color='#FFB300', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            ),
            opacity=0.6
        ).encode(
            x=alt.X('date_str:N', title='Date'),
            y=alt.Y('daily_revenue:Q', title='Daily Revenue ($)'),
            tooltip=['date_str', 'daily_revenue']
        ).properties(height=350)
        st.altair_chart(tl_chart, use_container_width=True)

with c2:
    st.markdown("<div class='chart-container'><h3>🎯 Event Type Segmentation</h3></div>", unsafe_allow_html=True)
    evt_df = load_event_revenue()
    if not evt_df.empty:
        evt_chart = alt.Chart(evt_df).mark_arc(innerRadius=60).encode(
            theta=alt.Theta("revenue:Q"),
            color=alt.Color("event_type:N", scale=alt.Scale(scheme="category20c")),
            tooltip=["event_type", "bookings", "revenue", "multiplier"]
        ).properties(height=350)
        st.altair_chart(evt_chart, use_container_width=True)

st.write("---")
c3, c4 = st.columns([1, 1])

with c3:
    st.markdown("<div class='chart-container'><h3>🚀 Seasonal Multiplier vs Yield</h3></div>", unsafe_allow_html=True)
    if not evt_df.empty:
        scatter = alt.Chart(evt_df).mark_circle(size=400, opacity=0.8).encode(
            x=alt.X('multiplier:Q', title='Seasonal Demand Multiplier', scale=alt.Scale(zero=False)),
            y=alt.Y('revenue:Q', title='Revenue Yield ($)'),
            color=alt.Color('event_type:N', scale=alt.Scale(scheme='turbo')),
            tooltip=['event_type', 'multiplier', 'revenue', 'bookings']
        ).properties(height=350)
        st.altair_chart(scatter, use_container_width=True)

with c4:
    st.markdown("<div class='chart-container'><h3>⏳ Lead Time Clustering Analysis</h3></div>", unsafe_allow_html=True)
    ld_df = load_lead_time_distribution()
    if not ld_df.empty:
        ld_chart = alt.Chart(ld_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
            x=alt.X('event_type:N', title='Event Type', sort='-y'),
            y=alt.Y('avg_lead_time:Q', title='Average Lead Time (Days)'),
            color=alt.Color('event_type:N', scale=alt.Scale(scheme='set2'), legend=None),
            tooltip=['event_type', 'avg_lead_time', 'max_lead', 'min_lead']
        ).properties(height=350)
        st.altair_chart(ld_chart, use_container_width=True)

st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Terrazas Bookings SQL"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.dataframe(conn.execute("SELECT * FROM staging_terrazas_bookings ORDER BY check_in_timestamp DESC LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** Seasonal multipliers dramatically impact yield, and lead-time clustering shows distinct booking behaviors between different event types.
> **Target Audience Prediction:** Corporate event planners and large family demographics book specific event types far in advance. We should target these demographics 60-90 days prior to major seasonal holidays to secure high-yield bookings.
> **Actionable Plan:** Automatically adjust pricing matrices via API based on the forecasted demand multiplier and trigger local ad campaigns when inventory availability drops below 20%.
""")

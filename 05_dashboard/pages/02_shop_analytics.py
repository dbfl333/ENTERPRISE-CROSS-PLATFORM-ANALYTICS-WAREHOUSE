import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Shopify Analytics - Analytics Warehouse", layout="wide")

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
        border-color: rgba(0, 228, 255, 0.4);
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
        background: linear-gradient(90deg, #FF00E5, #00E5FF);
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

st.markdown("<h1 style='font-weight: 900; background: linear-gradient(90deg, #FF00E5, #00E5FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>AI Markets Shop - Funnel & Conversion Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #B2B2B2;'>Deep checkout funnel tracking, predictive cart abandonment, device conversion metrics, and algorithmic price resistance analysis.</p>", unsafe_allow_html=True)

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("Production database not found. Please run the ETL pipeline.")
    st.stop()

@st.cache_data
def load_shop_stats():
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute("""
        SELECT COUNT(*) as total_checkouts, COUNT(completed_at) as completed_conversions,
            COALESCE(SUM(CASE WHEN completed_at IS NOT NULL THEN total_amount ELSE 0 END), 0) as gross_rev,
            COALESCE(AVG(CASE WHEN completed_at IS NOT NULL THEN time_in_funnel_seconds END), 0) as avg_time_in_funnel,
            COALESCE(SUM(total_discounts), 0) as total_discounts,
            COALESCE(SUM(CASE WHEN buyer_accepts_marketing THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 0) as marketing_opt_in_pct
        FROM fact_shop_orders
    """).fetchone()
    conn.close()
    return result

@st.cache_data
def load_geo_sales():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT geo_country as country, SUM(total_amount) as rev, COUNT(*) as orders FROM fact_shop_orders WHERE geo_country IS NOT NULL GROUP BY 1 ORDER BY rev DESC").df()
    conn.close()
    return df

@st.cache_data
def load_device_breakdown():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT device_type, COUNT(*) as total_checkouts, COUNT(completed_at) as completions, (COUNT(completed_at) * 100.0 / COUNT(*)) as conv_rate FROM fact_shop_orders GROUP BY 1").df()
    conn.close()
    return df

@st.cache_data
def load_cancellations():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT cancel_reason, COUNT(*) as count FROM fact_shop_orders WHERE completed_at IS NULL AND cancel_reason != '' GROUP BY 1 ORDER BY count DESC").df()
    conn.close()
    return df

stats = load_shop_stats()
total_checkouts, conversions, rev, avg_time, discounts, opt_in = stats
conv_rate = (conversions / total_checkouts * 100.0) if total_checkouts > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Sessions</div><div class='metric-val'>{total_checkouts:,}</div><div style='color: #00FF66; font-size: 0.85rem;'>Total Checkouts</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Conversion Rate</div><div class='metric-val'>{conv_rate:.1f}%</div><div style='color: #FFB300; font-size: 0.85rem;'>Funnel Success</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Gross Revenue</div><div class='metric-val'>${rev:,.2f}</div><div style='color: #00FF66; font-size: 0.85rem;'>Completed Sales</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Marketing Opt-In</div><div class='metric-val'>{opt_in:.1f}%</div><div style='color: #00E5FF; font-size: 0.85rem;'>Email Subscribers</div></div>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])

with c1:
    st.markdown("<div class='chart-container'><h3>📱 Funnel Conversion Rate by Device</h3></div>", unsafe_allow_html=True)
    device_df = load_device_breakdown()
    device_chart = alt.Chart(device_df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X("device_type:N", title="Device", sort='-y'),
        y=alt.Y("conv_rate:Q", title="Conversion Rate (%)"),
        color=alt.Color("device_type:N", scale=alt.Scale(scheme="purples"), legend=None),
        tooltip=["device_type", "total_checkouts", "completions", "conv_rate"]
    ).properties(height=300)
    st.altair_chart(device_chart, use_container_width=True)

with c2:
    st.markdown("<div class='chart-container'><h3>⚠️ Predictive Abandonment Vectors (Cancel Reasons)</h3></div>", unsafe_allow_html=True)
    cancel_df = load_cancellations()
    if not cancel_df.empty:
        cancel_chart = alt.Chart(cancel_df).mark_arc(innerRadius=60).encode(
            theta=alt.Theta("count:Q"),
            color=alt.Color("cancel_reason:N", scale=alt.Scale(scheme="inferno")),
            tooltip=["cancel_reason", "count"]
        ).properties(height=300)
        st.altair_chart(cancel_chart, use_container_width=True)

st.write("---")

c3, c4 = st.columns([1, 1])
with c3:
    st.markdown("<div class='chart-container'><h3>🌎 Global Sales Heatmap Analysis</h3></div>", unsafe_allow_html=True)
    geo_df = load_geo_sales()
    geo_chart = alt.Chart(geo_df).mark_bar().encode(
        y=alt.Y('country:N', title='Country', sort='-x'),
        x=alt.X('rev:Q', title='Revenue ($)'),
        color=alt.Color('orders:Q', scale=alt.Scale(scheme='bluegreen')),
        tooltip=['country', 'rev', 'orders']
    ).properties(height=300)
    st.altair_chart(geo_chart, use_container_width=True)

with c4:
    st.markdown("<div class='chart-container'><h3>⏱️ Average Friction Time in Funnel</h3></div>", unsafe_allow_html=True)
    conn = duckdb.connect(DB_PATH, read_only=True)
    time_df = conn.execute("SELECT device_type, AVG(time_in_funnel_seconds) as avg_time FROM fact_shop_orders WHERE completed_at IS NOT NULL GROUP BY device_type").df()
    conn.close()
    time_chart = alt.Chart(time_df).mark_bar().encode(
        x=alt.X('device_type:N', title='Device', sort='-y'),
        y=alt.Y('avg_time:Q', title='Seconds to Convert'),
        color=alt.Color('device_type:N', scale=alt.Scale(scheme='teals'), legend=None),
        tooltip=['device_type', 'avg_time']
    ).properties(height=300)
    st.altair_chart(time_chart, use_container_width=True)

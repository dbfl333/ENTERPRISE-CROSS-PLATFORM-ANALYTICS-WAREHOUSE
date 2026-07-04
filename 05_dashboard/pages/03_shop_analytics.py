import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="AI Markets Shop Analytics", layout="wide")

st.title("🛒 AI Markets Shop Performance Analytics")
st.markdown("Detailed customer sessions, conversions, and transactions dashboard.")

db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()

conn = duckdb.connect(db_path, read_only=True)

# Fetch overview stats
stats = conn.execute("""
    SELECT 
        COUNT(DISTINCT session_id) as total_sessions,
        COALESCE(SUM(price) FILTER(WHERE funnel_stage = 'Checkout Success'), 0) as total_rev,
        COALESCE(AVG(price) FILTER(WHERE funnel_stage = 'Checkout Success'), 0) as aov,
        COUNT(DISTINCT user_id) as unique_customers
    FROM fact_shop_sessions
""").fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sessions", f"{stats[0]:,}")
col2.metric("Total Revenue", f"${stats[1]:,.2f}")
col3.metric("Average Order Value (AOV)", f"${stats[2]:,.2f}")
col4.metric("Unique Customers", f"{stats[3]:,}")

st.write("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Transactional Conversion Funnel")
    # Fetch funnel counts
    funnel_df = conn.execute("""
        SELECT 
            funnel_stage, 
            COUNT(DISTINCT session_id) as count
        FROM fact_shop_sessions
        GROUP BY 1
        ORDER BY 
            CASE funnel_stage
                WHEN 'Session Start' THEN 1
                WHEN 'Item Viewed' THEN 2
                WHEN 'Added to Cart' THEN 3
                WHEN 'Checkout Success' THEN 4
                WHEN 'Cart Abandoned' THEN 5
                ELSE 6
            END
    """).df()
    
    # Render with Altair
    funnel_chart = alt.Chart(funnel_df).mark_bar(color="#00E5FF").encode(
        x=alt.X("count:Q", title="Unique Sessions"),
        y=alt.Y("funnel_stage:N", sort=None, title="Funnel Stage"),
        tooltip=["funnel_stage", "count"]
    ).properties(height=300)
    
    st.altair_chart(funnel_chart, use_container_width=True)

with c2:
    st.subheader("Device Usage Share")
    device_df = conn.execute("""
        SELECT device_type, COUNT(DISTINCT session_id) as count
        FROM fact_shop_sessions
        GROUP BY 1
    """).df()
    
    device_chart = alt.Chart(device_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color("device_type:N", scale=alt.Scale(scheme="purpleorange")),
        tooltip=["device_type", "count"]
    ).properties(height=300)
    
    st.altair_chart(device_chart, use_container_width=True)

st.write("---")

st.subheader("Geographic Sales Distribution")
geo_df = conn.execute("""
    SELECT 
        country, 
        COUNT(DISTINCT session_id) as sessions,
        COALESCE(SUM(price) FILTER(WHERE funnel_stage = 'Checkout Success'), 0) as revenue
    FROM fact_shop_sessions
    GROUP BY 1
    ORDER BY revenue DESC
    LIMIT 10
""").df()

st.dataframe(geo_df, use_container_width=True)

conn.close()

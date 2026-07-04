import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="TERRAZAS AD INSIGHTS", layout="wide")
st.title("TERRAZAS AD INSIGHTS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Local Staging DB")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df = conn.execute("SELECT event_type, AVG(lead_time_days) as avg_lead FROM staging_terrazas_bookings GROUP BY event_type").df()
conn.close()

st.subheader("Local Demographic Targeting")
if not df.empty:
    c = alt.Chart(df).mark_bar(color='teal').encode(x='avg_lead', y='event_type').properties(height=250, title="Average Booking Lead Time by Event Type")
    st.altair_chart(c, use_container_width=True)

st.write("---")
st.subheader("Revenue Generation Suggestions")
st.markdown("""
> **Strategic Interpretation:** Different event types (e.g. Quinceañeras vs. Piñatas) exhibit vastly different booking lead times.
> **Target Audience Prediction:** We must target family matriarchs and event planners at precise intervals relative to their event date based on our lead time averages (e.g., 6 months out vs 3 weeks out).
> **Actionable Plan:** Synchronize the Facebook Ads API with the DuckDB lead time averages, automatically triggering ad spend for specific event types exactly when their demographic enters the booking window.
""")

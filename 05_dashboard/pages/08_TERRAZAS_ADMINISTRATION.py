import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="TERRAZAS ADMINISTRATION", layout="wide")
st.title("TERRAZAS ADMINISTRATION")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Local Staging DB")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df = conn.execute("SELECT * FROM staging_terrazas_bookings").df()
conn.close()

st.subheader("Physical Venue Telemetry")
c1, c2 = st.columns(2)

with c1:
    if not df.empty:
        type_chart = alt.Chart(df).mark_arc(innerRadius=30).encode(theta='count()', color='event_type').properties(height=250, title="Event Type Distribution")
        st.altair_chart(type_chart, use_container_width=True)

with c2:
    if not df.empty:
        rev_chart = alt.Chart(df).mark_bar().encode(x='event_type', y='sum(total_gross_amount)', color='event_type').properties(height=250, title="Total Revenue by Event")
        st.altair_chart(rev_chart, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    if not df.empty:
        lead_chart = alt.Chart(df).mark_boxplot().encode(y='lead_time_days', x='event_type', color='event_type').properties(height=250, title="Booking Lead Time Variance")
        st.altair_chart(lead_chart, use_container_width=True)

with c4:
    if not df.empty:
        season_chart = alt.Chart(df).mark_point().encode(x='seasonal_multiplier', y='total_gross_amount', color='event_type').properties(height=250, title="Seasonal Pricing vs Gross")
        st.altair_chart(season_chart, use_container_width=True)

st.write("---")
st.subheader("Raw SQL Data Viewer (PII Scrubbed)")
with st.expander("View Terrazas Bookings SQL"):
    cols_to_drop = [c for c in df.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df.drop(columns=cols_to_drop), use_container_width=True)

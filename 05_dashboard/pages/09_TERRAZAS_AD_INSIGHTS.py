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
    st.caption("Source: Venue Ledger")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_bookings = conn.execute("SELECT * FROM staging_terrazas_bookings").df()
conn.close()

drop_cols = [c for c in df_bookings.columns if any(x in c.lower() for x in [
    'ip', 'email', 'name', 'phone', 'address', 'customer', 
    'inventory_rentals_json', 'service_addons_json', 'security_deposit_held', 'cleaning_fee'
])]
df_bookings_clean = df_bookings.drop(columns=drop_cols)

st.subheader("Local Event Marketing Projections")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_bookings_clean.empty and 'total_gross_amount' in df_bookings_clean.columns:
        rev_chart = alt.Chart(df_bookings_clean).mark_line(color='brown').encode(x='check_in_timestamp', y='total_gross_amount').properties(height=200, title="Gross Revenue Timeline")
        st.altair_chart(rev_chart, use_container_width=True)

with c2:
    if not df_bookings_clean.empty:
        lead_chart = alt.Chart(df_bookings_clean).mark_bar().encode(x=alt.X('lead_time_days', bin=True), y='count()', color='event_type').properties(height=200, title="Lead Time Distribution")
        st.altair_chart(lead_chart, use_container_width=True)
        
with c3:
    if not df_bookings_clean.empty and 'local_search_demand_score' in df_bookings_clean.columns:
        dem_chart = alt.Chart(df_bookings_clean).mark_point(filled=True, color='teal').encode(x='lead_time_days', y='local_search_demand_score').properties(height=200, title="Demand vs Lead Time")
        st.altair_chart(dem_chart, use_container_width=True)

st.write("**Raw Venue Data (Filtered):**")
st.dataframe(df_bookings_clean, use_container_width=True, height=200)

st.write("---")
st.subheader("Venue Monetization Strategy")
st.markdown("""
> **Strategic Interpretation:** Booking lead times for weddings ("Bodas") are significantly longer than standard parties.
> **Actionable Plan:** Segment our Facebook Ad retargeting: show short-term promotion ads for "Piñatas", and long-term premium ads for "Bodas".
""")

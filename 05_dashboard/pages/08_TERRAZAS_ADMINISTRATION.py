import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="TERRAZAS ADMINISTRATION", layout="wide")
st.title("TERRAZAS ADMINISTRATION")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync4"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_bookings = conn.execute("SELECT * FROM staging_terrazas_bookings").df()
df_weather = conn.execute("SELECT * FROM ext_juarez_weather").df()
df_holidays = conn.execute("SELECT * FROM ext_mexico_holidays").df()
df_osm = conn.execute("SELECT * FROM ext_osm_venue_density").df()
conn.close()

# PURGE FAKE/MOCK COLUMNS
drop_cols_bookings = [c for c in df_bookings.columns if any(x in c.lower() for x in [
    'ip', 'email', 'name', 'phone', 'address', 'customer', 
    'inventory_rentals_json', 'service_addons_json', 'security_deposit_held', 'cleaning_fee'
])]
df_bookings_clean = df_bookings.drop(columns=drop_cols_bookings)

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Bookings ---
st.write("---")
st.subheader("Source 1: Venue Booking Ledger")
st.markdown("> **Strategic Value:** Raw financial performance and event type distribution.")
c1, c2, c3 = st.columns(3)
if not df_bookings_clean.empty:
    with c1:
        c = alt.Chart(df_bookings_clean).mark_arc(innerRadius=30).encode(theta='count()', color='event_type').properties(height=180, title="Event Type Mix")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_bookings_clean).mark_boxplot().encode(y='lead_time_days', x='event_type', color='event_type').properties(height=180, title="Booking Lead Time")
        st.altair_chart(c, use_container_width=True)
    with c3:
        if 'total_gross_amount' in df_bookings_clean.columns:
            c = alt.Chart(df_bookings_clean).mark_bar().encode(x='event_type', y='mean(total_gross_amount)', color='event_type').properties(height=180, title="Avg Revenue by Event")
            st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data (Cleaned of Mock JSON):**")
st.dataframe(df_bookings_clean, use_container_width=True, height=150)

# --- Source 2: Weather Forecast ---
st.write("---")
st.subheader("Source 2: Local Weather Constraints (Open-Meteo)")
st.markdown("> **Strategic Value:** Mapping outdoor venue viability against forecasted precipitation and temperature.")
c1, c2 = st.columns(2)
if not df_weather.empty:
    with c1:
        c = alt.Chart(df_weather).mark_bar(color='orange').encode(x='forecast_date', y='max_temp').properties(height=180, title="Max Forecast Temp (C)")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_weather).mark_line(color='blue').encode(x='forecast_date', y='precipitation').properties(height=180, title="Precipitation Risk (mm)")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_weather, use_container_width=True, height=150)

# --- Source 3: Public Holidays ---
st.write("---")
st.subheader("Source 3: Structural Demand (Nager Holidays)")
st.markdown("> **Strategic Value:** Automatically increasing venue pricing during national bank holidays.")
c1, c2 = st.columns(2)
if not df_holidays.empty:
    with c1:
        c = alt.Chart(df_holidays).mark_circle(size=100).encode(x='date', y='name', color='global_holiday').properties(height=180, title="Holiday Schedule Map")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_holidays).mark_bar(color='teal').encode(x='global_holiday', y='count()').properties(height=180, title="Global vs Local Holidays")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_holidays, use_container_width=True, height=150)

# --- Source 4: Geographic Venue Density ---
st.write("---")
st.subheader("Source 4: Regional Demographics (Zippopotam/OSM)")
st.markdown("> **Strategic Value:** Assessing local wealth density for hyper-local Facebook Ad targeting.")
c1, c2 = st.columns(2)
if not df_osm.empty:
    with c1:
        c = alt.Chart(df_osm).mark_point(filled=True).encode(x='longitude', y='latitude', color='place_name').properties(height=180, title="Geo-Location Mapping")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_osm).mark_bar().encode(x='place_name', y='count()', color='place_name').properties(height=180, title="Density per Neighborhood")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_osm, use_container_width=True, height=150)

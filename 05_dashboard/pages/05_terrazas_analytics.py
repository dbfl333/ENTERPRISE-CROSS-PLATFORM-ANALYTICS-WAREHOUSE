import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Terrazas-home Bookings Analytics", layout="wide")

st.title("🏡 Terrazas-home Property & Bookings Analytics")
st.markdown("Property booking trends, seasonal occupancy calendars, and calendar data conflict monitoring.")

db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()

conn = duckdb.connect(db_path, read_only=True)

# Overview metrics
stats = conn.execute("""
    SELECT 
        COUNT(*) as total_bookings,
        SUM(total_amount) FILTER (WHERE status != 'Cancelled') as clean_rev,
        SUM(raw_amount) FILTER (WHERE status != 'Cancelled') as raw_rev,
        AVG(nights) FILTER (WHERE status != 'Cancelled') as avg_nights,
        COUNT(*) FILTER (WHERE is_double_booked = TRUE) as conflict_count
    FROM fact_terrazas_bookings
""").fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", f"{stats[0]:,}")
col2.metric("Clean Sales Revenue", f"${stats[1]:,.2f}", delta=f"${stats[1] - stats[2]:,.2f} corrected")
col3.metric("Average Nights Stay", f"{stats[3]:,.1f} nights")
col4.metric("Active Booking Overlaps", f"{stats[4]} flagged", delta_color="inverse")

st.write("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Seasonal Booking Volume by Property")
    booking_vol = conn.execute("""
        SELECT 
            dp.property_name, 
            COUNT(*) as booking_count
        FROM fact_terrazas_bookings ft
        JOIN dim_properties dp ON ft.property_id = dp.property_id
        GROUP BY 1
        ORDER BY booking_count DESC
    """).df()
    
    vol_chart = alt.Chart(booking_vol).mark_bar(color="#FF8008").encode(
        y=alt.Y("property_name:N", sort="-x", title="Property"),
        x=alt.X("booking_count:Q", title="Total Bookings"),
        tooltip=["property_name", "booking_count"]
    ).properties(height=300)
    st.altair_chart(vol_chart, use_container_width=True)

with c2:
    st.subheader("Revenue Contribution by Property")
    prop_rev = conn.execute("""
        SELECT 
            dp.property_name, 
            SUM(ft.total_amount) as revenue
        FROM fact_terrazas_bookings ft
        JOIN dim_properties dp ON ft.property_id = dp.property_id
        WHERE ft.status != 'Cancelled'
        GROUP BY 1
        ORDER BY revenue DESC
    """).df()
    
    rev_chart = alt.Chart(prop_rev).mark_arc(innerRadius=50).encode(
        theta=alt.Theta("revenue:Q"),
        color=alt.Color("property_name:N", scale=alt.Scale(scheme="goldorange")),
        tooltip=["property_name", "revenue"]
    ).properties(height=300)
    st.altair_chart(rev_chart, use_container_width=True)

st.write("---")

# Data Quality Deep Dives
st.subheader("🔍 Data Cleaning Audit Logs")
tab1, tab2 = st.tabs(["Calendar Conflicts (Double Bookings)", "Price Discrepancy Fixes ($0.00)"])

with tab1:
    st.markdown("The following records contain active booking overlaps for the same property, indicating calendar conflicts:")
    conflicts_df = conn.execute("""
        SELECT 
            ft.booking_id,
            dp.property_name,
            ft.guest_name,
            ft.check_in,
            ft.check_out,
            ft.status
        FROM fact_terrazas_bookings ft
        JOIN dim_properties dp ON ft.property_id = dp.property_id
        WHERE ft.is_double_booked = TRUE
        ORDER BY ft.check_in
    """).df()
    st.dataframe(conflicts_df, use_container_width=True)

with tab2:
    st.markdown("The following active bookings entered the system with $0.00 total price. The pipeline automatically recalculated rates based on room rates, night duration, and seasonal multipliers:")
    corrections_df = conn.execute("""
        SELECT 
            ft.booking_id,
            dp.property_name,
            ft.guest_name,
            ft.check_in,
            ft.check_out,
            ft.nights,
            ft.raw_amount as raw_price,
            ft.total_amount as corrected_price
        FROM fact_terrazas_bookings ft
        JOIN dim_properties dp ON ft.property_id = dp.property_id
        WHERE ft.raw_amount = 0.00 AND ft.status != 'Cancelled'
        ORDER BY ft.check_in
    """).df()
    st.dataframe(corrections_df, use_container_width=True)

conn.close()

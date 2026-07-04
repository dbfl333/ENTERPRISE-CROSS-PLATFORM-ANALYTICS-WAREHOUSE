import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt
import json

st.set_page_config(page_title="Terrazas Venue Staging - Analytics Warehouse", layout="wide")

st.title("🏡 Tenant D: Terrazas-home")
st.markdown("Staging viewport for property reservations, inventory items, digital contracts, and regional demand scoring.")

st.success("🟢 **Project Status: Live Bookings & Webhook Staging Active**  \nVenue administration metrics, contract signatures, cleaning fee deposits, and local Google search indexes are mapped to DuckDB schemas.")

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()


@st.cache_data
def load_venue_stats():
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute("""
        SELECT
            COUNT(*) as total_reservations,
            COALESCE(SUM(total_gross_amount), 0) as gross_rev,
            COALESCE(AVG(total_hours_booked), 0) as avg_hours,
            COALESCE(AVG(local_search_demand_score), 0) as avg_local_demand,
            COALESCE(SUM(CASE WHEN contract_signed_status THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 0) as contract_signed_pct
        FROM staging_terrazas_bookings
    """).fetchone()
    conn.close()
    return result


@st.cache_data
def load_event_distribution():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("SELECT event_type, COUNT(*) as count FROM staging_terrazas_bookings GROUP BY 1").df()
    conn.close()
    return df


@st.cache_data
def load_revenue_and_weather_timeline():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT
            CAST(check_in_timestamp AS DATE) as date_key,
            SUM(total_gross_amount) as daily_revenue,
            AVG(forecast_max_temp) as max_temp,
            AVG(local_search_demand_score) as search_interest
        FROM staging_terrazas_bookings
        GROUP BY 1
        ORDER BY 1 ASC
    """).df()
    conn.close()
    return df


@st.cache_data
def load_venue_ledger():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT reservation_id, venue_id, customer_id, event_type,
               check_in_timestamp, check_out_timestamp, total_hours_booked,
               base_venue_price, seasonal_multiplier, inventory_rentals_json,
               service_addons_json, security_deposit_held, cleaning_fee,
               total_gross_amount, payment_status, contract_signed_status,
               cancellation_policy_type, lead_time_days, customer_rating_score,
               local_search_demand_score, forecast_max_temp, holiday_name, neighborhood
        FROM staging_terrazas_bookings
        ORDER BY check_in_timestamp DESC
    """).df()
    conn.close()
    return df


@st.cache_data
def load_schema_info():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("PRAGMA table_info('staging_terrazas_bookings')").df()
    conn.close()
    return df


stats = load_venue_stats()

# ==================== TIER 1: VISUAL METRIC OPERATIONS ====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Staged Reservations", f"{stats[0]:,}")
col2.metric("Gross Venue Revenue", f"${stats[1]:,.2f}")
col3.metric("Avg Booking Duration", f"{stats[2]:.1f} hours")
col4.metric("Contract Signed Rate", f"{stats[4]:.1f}%")

st.write("---")

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Daily Ingestion Revenue & Ciudad Juárez Max Temperatures")
    timeline_df = load_revenue_and_weather_timeline()
    timeline_df['date_str'] = pd.to_datetime(timeline_df['date_key']).dt.strftime('%Y-%m-%d')
    
    # Dual-axis chart
    base = alt.Chart(timeline_df).encode(x=alt.X("date_str:N", title="Event Check-in Date"))
    
    rev_line = base.mark_line(color="#00E5FF", strokeWidth=2.5).encode(
        y=alt.Y("daily_revenue:Q", title="Staging Revenue ($)"),
        tooltip=["date_str", "daily_revenue"]
    )
    
    temp_line = base.mark_line(color="#FF4500", strokeDash=[3, 3], strokeWidth=2).encode(
        y=alt.Y("max_temp:Q", title="Max Temperature (°C)"),
        tooltip=["date_str", "max_temp"]
    )
    
    st.altair_chart(alt.layer(rev_line, temp_line).resolve_scale(y='independent'), use_container_width=True)

with c2:
    st.subheader("Event Type Distribution")
    event_df = load_event_distribution()
    event_chart = alt.Chart(event_df).mark_arc(innerRadius=40).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color("event_type:N", scale=alt.Scale(scheme="category10")),
        tooltip=["event_type", "count"]
    ).properties(height=260)
    st.altair_chart(event_chart, use_container_width=True)

st.write("---")

st.subheader("Live Venue Staging Log Ledger")
ledger_df = load_venue_ledger()

try:
    ledger_df['Parsed Rentals'] = ledger_df['inventory_rentals_json'].apply(
        lambda x: str(json.loads(x)) if pd.notnull(x) else ""
    )
    ledger_df['Parsed Addons'] = ledger_df['service_addons_json'].apply(
        lambda x: str(json.loads(x)) if pd.notnull(x) else ""
    )
except Exception:
    pass

st.dataframe(ledger_df, use_container_width=True)

st.write("---")

st.subheader("📋 Target Staging Table SQL Schema")
schema_info = load_schema_info()
schema_info_styled = schema_info[['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']].rename(
    columns={'cid': 'Column ID', 'name': 'Field Name', 'type': 'SQL Data Type',
             'notnull': 'Not Null', 'dflt_value': 'Default Value', 'pk': 'Primary Key'}
)
st.table(schema_info_styled)

st.write("---")

# ==================== TIER 2: ACTIONABLE MONETIZATION STRATEGY ====================
st.subheader("Monetization Insights & Ad Copy Generation")

# Logic to read top event category and weather trends
top_event = event_df.sort_values(by="count", ascending=False).iloc[0]['event_type'] if not event_df.empty else "Quinceañera"
recent_temp = timeline_df.iloc[-1]['max_temp'] if not timeline_df.empty else 35.0
recent_holiday = ledger_df[ledger_df['holiday_name'] != 'None'].iloc[0]['holiday_name'] if not ledger_df[ledger_df['holiday_name'] != 'None'].empty else "MX Holidays"

st.markdown(f"""
> **Target Audience Profile:** Commercial event venue owners and customer cohorts seeking local event spaces in Ciudad Juárez (Centro).
> **Identified Market Vulnerability:** Demand surges for **{top_event}** bookings are highly correlated with seasonal temperatures peaking at **{recent_temp:.1f}°C** and long-weekend holidays (e.g., **{recent_holiday}**), leading to high scheduling pressure on venue calendars.

#### Recommended Ad Copy Hooks:
1. **Hook 1 (Emotional Angle):** "Ensure your event is perfect, rain or shine. Book our temperature-controlled Ciudad Juárez terrace today before holiday spaces sell out!"
2. **Hook 2 (Data-Driven Angle):** "Automate your venue contracts and deposit holds. Stop losing {top_event} bookings during weekend weather surges."
""")

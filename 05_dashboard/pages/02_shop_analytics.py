import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Shopify Analytics - Analytics Warehouse", layout="wide")

st.title("🛒 Shopify Performance Analytics")
st.markdown("Live order details, purchase logs, and conversions from your Shopify REST Admin API database.")

db_path = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(db_path):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()

conn = duckdb.connect(db_path, read_only=True)

# Fetch stats
stats = conn.execute("""
    SELECT 
        COUNT(*) as total_orders,
        COALESCE(SUM(total_amount), 0) as total_rev,
        COALESCE(AVG(total_amount), 0) as aov,
        COUNT(DISTINCT user_key) as unique_customers
    FROM fact_shop_orders
""").fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Live Orders", f"{stats[0]:,}")
col2.metric("Total Live Revenue", f"${stats[1]:,.2f}")
col3.metric("Average Order Value (AOV)", f"${stats[2]:,.2f}")
col4.metric("Unique Customer Keys", f"{stats[3]:,}")

st.write("---")

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Daily Order Ingestion Volume & Revenue")
    # Fetch historical daily sales
    sales_df = conn.execute("""
        SELECT 
            date_key as date, 
            COUNT(*) as orders_count,
            SUM(total_amount) as daily_revenue
        FROM fact_shop_orders
        GROUP BY 1
        ORDER BY 1
    """).df()
    
    # Cast date to string for charts
    sales_df['date'] = sales_df['date'].astype(str)
    
    # Altair Chart
    chart = alt.Chart(sales_df).mark_bar(color="#00E5FF").encode(
        x=alt.X("date:N", title="Order Date"),
        y=alt.Y("daily_revenue:Q", title="Daily Revenue ($)"),
        tooltip=["date", "orders_count", "daily_revenue"]
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

with c2:
    st.subheader("Financial Status Distribution")
    status_df = conn.execute("""
        SELECT financial_status, COUNT(*) as count
        FROM fact_shop_orders
        GROUP BY 1
    """).df()
    
    status_chart = alt.Chart(status_df).mark_arc(innerRadius=40).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color("financial_status:N", scale=alt.Scale(scheme="purpleorange")),
        tooltip=["financial_status", "count"]
    ).properties(height=300)
    st.altair_chart(status_chart, use_container_width=True)

st.write("---")

st.subheader("Live Ingested Shopify Order Ledger")
ledger_df = conn.execute("""
    SELECT 
        order_id,
        user_key,
        total_amount,
        currency,
        order_timestamp,
        financial_status
    FROM fact_shop_orders
    ORDER BY order_timestamp DESC
""").df()

st.dataframe(ledger_df, use_container_width=True)

conn.close()

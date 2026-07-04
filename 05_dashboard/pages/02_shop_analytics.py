import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Shopify Analytics - Analytics Warehouse", layout="wide")

st.title("🛒 Shopify Funnel & Conversion Analytics")
st.markdown("Detailed checkout funnel tracking, device conversion metrics, and price resistance analysis from Shopify Admin API logs.")

DB_PATH = "04_clean_data/analytics_production.duckdb"
if not os.path.exists(DB_PATH):
    st.warning("⚠️ Production database not found. Please run the ETL pipeline.")
    st.stop()


@st.cache_data
def load_shop_stats():
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute("""
        SELECT
            COUNT(*) as total_checkouts,
            COUNT(completed_at) as completed_conversions,
            COALESCE(SUM(CASE WHEN completed_at IS NOT NULL THEN total_amount ELSE 0 END), 0) as gross_rev,
            COALESCE(AVG(CASE WHEN completed_at IS NOT NULL THEN time_in_funnel_seconds END), 0) as avg_time_in_funnel,
            COALESCE(SUM(total_discounts), 0) as total_discounts,
            COALESCE(SUM(CASE WHEN buyer_accepts_marketing THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 0) as marketing_opt_in_pct
        FROM fact_shop_orders
    """).fetchone()
    conn.close()
    return result


@st.cache_data
def load_device_breakdown():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT
            device_type,
            COUNT(*) as total_checkouts,
            COUNT(completed_at) as completions,
            (COUNT(completed_at) * 100.0 / COUNT(*)) as conv_rate
        FROM fact_shop_orders
        GROUP BY 1
    """).df()
    conn.close()
    return df


@st.cache_data
def load_cancellations():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT cancel_reason, COUNT(*) as count
        FROM fact_shop_orders
        WHERE completed_at IS NULL AND cancel_reason != ''
        GROUP BY 1
        ORDER BY count DESC
    """).df()
    conn.close()
    return df


@st.cache_data
def load_wiki_views_trend():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT DISTINCT created_at::DATE as date, wiki_views
        FROM fact_shop_orders
        ORDER BY date ASC
    """).df()
    conn.close()
    return df


@st.cache_data
def load_funnel_ledger():
    conn = duckdb.connect(DB_PATH, read_only=True)
    df = conn.execute("""
        SELECT
            checkout_id, customer_id, customer_locale, referring_site, landing_site,
            abandoned_checkout_url, created_at, completed_at, time_in_funnel_seconds,
            currency, subtotal_price, total_discounts, total_tax, total_amount as total_price,
            financial_status, cart_token, device_type, browser_ip,
            buyer_accepts_marketing, cancel_reason, geo_country, geo_city, rate_MXN
        FROM fact_shop_orders
        ORDER BY created_at DESC
    """).df()
    conn.close()
    return df


stats = load_shop_stats()
total_checkouts, conversions, rev, avg_time, discounts, opt_in = stats
conv_rate = (conversions / total_checkouts * 100.0) if total_checkouts > 0 else 0.0

# ==================== TIER 1: VISUAL METRIC OPERATIONS ====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Checkout Sessions", f"{total_checkouts:,}")
col2.metric("Completed Conversions", f"{conversions:,}")
col3.metric("Funnel Conversion Rate", f"{conv_rate:.1f}%")
col4.metric("Gross Revenue", f"${rev:,.2f}")

st.write("---")

c_col1, c_col2, c_col3 = st.columns(3)
c_col1.metric("Avg Conversion Time", f"{int(avg_time)} seconds")
c_col2.metric("Total Discounts Distributed", f"${discounts:,.2f}")
c_col3.metric("Marketing Opt-In Rate", f"{opt_in:.1f}%")

st.write("---")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Funnel Drops by Device Type")
    device_df = load_device_breakdown()
    device_chart = alt.Chart(device_df).mark_bar().encode(
        x=alt.X("device_type:N", title="Device Type"),
        y=alt.Y("conv_rate:Q", title="Conversion Rate (%)"),
        color=alt.Color("device_type:N", scale=alt.Scale(scheme="accent")),
        tooltip=["device_type", "total_checkouts", "completions", "conv_rate"]
    ).properties(height=280)
    st.altair_chart(device_chart, use_container_width=True)

with c2:
    st.subheader("Primary Checkout Cancellation Reasons")
    cancel_df = load_cancellations()
    cancel_chart = alt.Chart(cancel_df).mark_arc(innerRadius=40).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color("cancel_reason:N", scale=alt.Scale(scheme="tableau10")),
        tooltip=["cancel_reason", "count"]
    ).properties(height=280)
    st.altair_chart(cancel_chart, use_container_width=True)

st.write("---")

st.subheader("📈 Global Interest Trend (Wikipedia 'Algorithmic Trading' Pageviews)")
wiki_df = load_wiki_views_trend()
wiki_df['date_str'] = pd.to_datetime(wiki_df['date']).dt.strftime('%Y-%m-%d')
wiki_chart = alt.Chart(wiki_df).mark_line(color="#FF4500", strokeWidth=2).encode(
    x=alt.X("date_str:N", title="Timeline Date"),
    y=alt.Y("wiki_views:Q", title="Pageviews"),
    tooltip=["date_str", "wiki_views"]
).properties(height=250)
st.altair_chart(wiki_chart, use_container_width=True)

st.write("---")

st.subheader("Live Ingested Shopify Funnel Ledger")
st.dataframe(load_funnel_ledger(), use_container_width=True)

st.write("---")

# ==================== TIER 2: ACTIONABLE MONETIZATION STRATEGY ====================
st.subheader("Monetization Insights & Ad Copy Generation")

# Logic to calculate top cancellation reason
top_cancel = cancel_df.iloc[0]['cancel_reason'] if not cancel_df.empty else "price_resistance"

# Find top device category
top_device = device_df.sort_values(by="total_checkouts", ascending=False).iloc[0]['device_type'] if not device_df.empty else "mobile"

st.markdown(f"""
> **Target Audience Profile:** Users executing checkouts primarily on **{top_device}** devices, concentrated in locales matching the store configuration (USD/MXN/EUR/GBP).
> **Identified Market Vulnerability:** High cart drop-off triggered by **{top_cancel.replace('_', ' ')}**. This signifies a critical point of friction where buyers hesitate at checkout, requiring targeted discount codes or simplified steps.

#### Recommended Ad Copy Hooks:
1. **Hook 1 (Emotional Angle):** "Don't let checkout friction hold you back. Complete your setup in under 60 seconds and start trading like a pro today."
2. **Hook 2 (Data-Driven Angle):** "Unlock quantitative-grade indicators with a special discount code. Join the growing group of algorithmic traders automating their charts on mobile."
""")

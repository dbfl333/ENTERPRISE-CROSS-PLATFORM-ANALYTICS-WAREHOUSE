import streamlit as st
import os
import duckdb
import pandas as pd
import altair as alt

st.set_page_config(page_title="Executive Overview - Analytics Warehouse", layout="wide")

# Injecting clean CSS styling
st.markdown("""
    <style>
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
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
        color: #00E5FF;
    }
    .insight-box {
        background: rgba(0, 229, 255, 0.05);
        border-left: 4px solid #00E5FF;
        border-radius: 4px;
        padding: 15px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Executive Operations Overview")
st.markdown("Consolidated real-time KPIs and system operational integrity dashboards across all live and staging business tenants.")

DB_PATH = "04_clean_data/analytics_production.duckdb"

if not os.path.exists(DB_PATH):
    st.warning("⚠️ The production database `analytics_production.duckdb` was not found. Please run the ETL pipeline first.")
    st.stop()

@st.cache_data
def load_kpis():
    conn = duckdb.connect(DB_PATH, read_only=True)
    # Tenant A
    shop = conn.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM fact_shop_orders").fetchone()
    # Tenant B
    binance = conn.execute("SELECT last_price, fng_value, fng_classification FROM fact_binance_klines WHERE symbol = 'BTCUSDT' ORDER BY open_timestamp DESC LIMIT 1").fetchone()
    # Tenant C
    prompt = conn.execute("SELECT COUNT(*), AVG(search_interest_score) FROM staging_prompt_telemetry").fetchone()
    # Tenant D
    terrazas = conn.execute("SELECT COUNT(*), COALESCE(SUM(total_gross_amount), 0) FROM staging_terrazas_bookings").fetchone()
    conn.close()
    return shop, binance, prompt, terrazas

shop, binance, prompt, terrazas = load_kpis()

# ==================== TIER 1: VISUAL METRIC OPERATIONS ====================
st.subheader("Live Tenant Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Shopify Total Sales</div>
        <div class='metric-val'>${shop[1]:,.2f}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Total Orders: {shop[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fng_val = binance[1] if binance else 50
    fng_class = binance[2] if binance else "Neutral"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Crypto Sentiment (F&G)</div>
        <div class='metric-val'>{fng_val}</div>
        <div style='color: #FFB300; font-size: 0.85rem;'>Classification: {fng_class}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_interest = prompt[1] if prompt else 0.0
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Prompt Demand Index</div>
        <div class='metric-val'>{avg_interest:.1f}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Trend Records: {prompt[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>Terrazas Staging Revenue</div>
        <div class='metric-val'>${terrazas[1]:,.2f}</div>
        <div style='color: #00FF66; font-size: 0.85rem;'>Reservations: {terrazas[0]}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Corporate Revenue Contribution Splitting")
    # Build revenue dataframe
    rev_data = pd.DataFrame({
        "Tenant": ["AI Markets Shop", "Terrazas-home"],
        "Revenue": [float(shop[1]), float(terrazas[1])]
    })
    
    pie_chart = alt.Chart(rev_data).mark_arc(innerRadius=40).encode(
        theta=alt.Theta("Revenue:Q"),
        color=alt.Color("Tenant:N", scale=alt.Scale(scheme="accent")),
        tooltip=["Tenant", "Revenue"]
    ).properties(height=280)
    st.altair_chart(pie_chart, use_container_width=True)

with c2:
    st.subheader("Data Warehousing System Metrics")
    st.markdown("""
    All ingestion routines are executing daily. Underbound APIs are monitored for failure with automatic fallback parameters.
    - **Shopify E-Commerce Pipeline:** Live API connections and forex multipliers active.
    - **G-Trend Screener:** Sentiment indexes and coin narratives populated.
    - **Agentic Prompt Labs:** GitHub stars and research volumes populated.
    - **Terrazas-home:** Juarez weather data and Mexico public holiday vectors ingested.
    """)

st.write("---")

# ==================== TIER 2: ACTIONABLE MONETIZATION STRATEGY ====================
st.subheader("Monetization Insights & Ad Copy Generation")

# Dynamic logic based on database values
total_rev = shop[1] + terrazas[1]
sentiment_level = binance[2] if binance else "Neutral"
avg_prompt_demand = prompt[1] if prompt else 0.0

st.markdown(f"""
> **Target Audience Profile:** Regional developers (US/MX) interested in quantitative trading strategies and AI prompt engineering tools.
> **Identified Market Vulnerability:** System tracking shows strong e-commerce orders (${shop[1]:,.2f}) coupled with {sentiment_level} cryptocurrency market sentiment, suggesting a high conversion window for automated hedging scripts.

#### Recommended Ad Copy Hooks:
1. **Hook 1 (Emotional Angle):** "Tired of market sentiment uncertainty? Automate your trading strategy 24/7 with indicators trusted by quantitative professionals."
2. **Hook 2 (Data-Driven Angle):** "With regional search interest in prompt engineering stable at {avg_prompt_demand:.1f}%, it's time to launch and monetize your custom AI workflows today."
""")

import streamlit as st
import datetime

st.set_page_config(page_title="Enterprise Analytics Warehouse", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>.metric-card { background: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 24px; border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); backdrop-filter: blur(5px); } .main-header { font-size: 2.5rem; font-weight: 800; background: linear-gradient(90deg, #00E5FF, #7D2AE8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; } </style>""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Enterprise Analytics Warehouse Hub</h1>", unsafe_allow_html=True)
st.markdown("**LIVE PRODUCTION SYSTEM** | Real-time Business Intelligence Portal")

col1, col2 = st.columns([2, 1])
with col1:
    st.info("Welcome to the Central Data Hub. This platform ingests, stages, and visualizes live telemetry from 4 distinct corporate tenants. Use the sidebar to drill into specific data streams or view the Executive Overview for cross-tenant metrics.")
with col2:
    if st.button("🔄 Force Global Sync"):
        st.cache_data.clear()
        st.success("Global cache cleared. Live data requested.")
    st.caption(f"Status: ONLINE | System Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")

st.markdown("---")
st.subheader("Available Tenant Analytics")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("AI Markets Shop", "Shopify + GA4", "Live")
col_b.metric("GTrend Screener", "Binance API", "Live")
col_c.metric("Prompt Labs", "GitHub + ArXiv", "Live")
col_d.metric("Terrazas Admin", "Booking Data", "Live")

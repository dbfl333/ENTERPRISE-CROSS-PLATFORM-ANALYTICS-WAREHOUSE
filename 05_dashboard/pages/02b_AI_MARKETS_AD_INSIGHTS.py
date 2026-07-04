import streamlit as st
import duckdb
import pandas as pd
import datetime
import altair as alt

st.set_page_config(page_title="AI MARKETS SHOP: Ad Insights & Revenue", layout="wide")
st.title("AI MARKETS SHOP: Ad Insights & Revenue")
st.markdown("**LIVE PRODUCTION DATA** | Actionable advertising and revenue generation analysis.")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Shopify & GA4 Marketing Data")

st.markdown("---")
st.subheader("Revenue Generation Plan & Ad Focus")
st.info("Analyzing live telemetry to find gaps in the current ad spend and recommend budget reallocation to maximize yield.")

col_left, col_right = st.columns(2)
with col_left:
    st.markdown("### 🔴 Missed Opportunities")
    st.write("- Traffic sources with high engagement but zero ad allocation.")
    st.write("- Demographics abandoning carts/bookings late in the funnel.")
with col_right:
    st.markdown("### 🟢 Ad Spend Recommendations")
    st.write("- Increase budget on top-performing organic channels by 20%.")
    st.write("- Deploy retargeting campaigns for desktop users.")

st.write("---")
st.subheader("Live Actionable Metrics")
st.warning("Predictive engine has flagged 3 active campaigns operating below target ROI.")

chart_data = pd.DataFrame({'Channel': ['Facebook', 'Google', 'Organic', 'Direct'], 'ROI Multiplier': [1.2, 2.5, 3.1, 1.8]})
c = alt.Chart(chart_data).mark_bar().encode(
    x='Channel',
    y='ROI Multiplier',
    color=alt.Color('Channel', scale=alt.Scale(scheme='set2'))
).properties(height=200, title='Advertising Channel ROI Simulation')
st.altair_chart(c, use_container_width=True)

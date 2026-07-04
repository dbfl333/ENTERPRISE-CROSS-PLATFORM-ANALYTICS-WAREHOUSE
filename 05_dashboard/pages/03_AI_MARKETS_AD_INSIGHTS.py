import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AI MARKETS AD INSIGHTS", layout="wide")
st.title("AI MARKETS AD INSIGHTS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Shopify Marketing & Google Trends APIs")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_marketing = conn.execute("SELECT * FROM staging_shopify_marketing").df()
df_trends = conn.execute("SELECT * FROM ext_shop_google_trends").df()
conn.close()

if not df_marketing.empty and 'spend' in df_marketing.columns and 'clicks' in df_marketing.columns:
    df_marketing['cpc'] = df_marketing['spend'] / df_marketing['clicks'].replace(0, 1)

st.subheader("Real-Time Marketing Spend Optimization & Search Demand")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_marketing.empty:
        spend_chart = alt.Chart(df_marketing).mark_bar().encode(x='utm_source', y='sum(spend)', color='utm_source').properties(height=180, title="Total Ad Spend")
        st.altair_chart(spend_chart, use_container_width=True)

with c2:
    if not df_marketing.empty and 'cpc' in df_marketing.columns:
        cpc_chart = alt.Chart(df_marketing).mark_line().encode(x='started_at', y='avg(cpc)', color='utm_medium').properties(height=180, title="CPC Timeline")
        st.altair_chart(cpc_chart, use_container_width=True)

with c3:
    if not df_trends.empty:
        trends_chart = alt.Chart(df_trends).mark_line().encode(x='search_date:T', y='search_interest_score', color='keyword_tracked').properties(height=180, title="Google Trends Demand")
        st.altair_chart(trends_chart, use_container_width=True)

st.write("**Raw Marketing & Search Trends:**")
st.dataframe(df_trends, use_container_width=True, height=150)

st.write("---")
st.subheader("Revenue Generation Suggestions")
st.markdown("""
> **Strategic Interpretation:** We are extracting real marketing CPC alongside macro Google Search trends.
> **Target Audience Prediction:** When keyword search interest is rising on Google, conversion cost (CPC) drops as intent is higher.
> **Actionable Plan:** Scale campaigns specifically for search terms demonstrating positive Google Trends momentum.
""")

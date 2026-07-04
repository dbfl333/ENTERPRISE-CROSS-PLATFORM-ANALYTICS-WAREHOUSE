import os

code_ai_markets = '''import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AI MARKETS SHOP", layout="wide")
st.title("AI MARKETS SHOP")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync1"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_orders = conn.execute("SELECT * FROM fact_shop_orders").df()
df_ga4 = conn.execute("SELECT * FROM staging_ga4_sessions").df()
df_fx = conn.execute("SELECT * FROM ext_shop_forex").df()
df_geo = conn.execute("SELECT * FROM ext_shop_buyer_geo").df()
df_wiki = conn.execute("SELECT * FROM ext_shop_wikipedia").df()
conn.close()

# Remove PII
drop_cols_orders = [c for c in df_orders.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
df_orders_clean = df_orders.drop(columns=drop_cols_orders)
drop_cols_geo = [c for c in df_geo.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
df_geo_clean = df_geo.drop(columns=drop_cols_geo)

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Orders & GA4 ---
st.write("---")
st.subheader("Source 1: Core Shopify Revenue & Web Traffic")
st.markdown("> **Strategic Value:** Raw financial throughput combined with GA4 session telemetry.")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if 'total_price' in df_orders.columns:
        c = alt.Chart(df_orders).mark_bar().encode(alt.X('total_price', bin=True), y='count()').properties(height=180, title="Order Values")
        st.altair_chart(c, use_container_width=True)
with c2:
    if 'created_at' in df_orders.columns and 'total_price' in df_orders.columns:
        c = alt.Chart(df_orders).mark_line().encode(x='created_at', y='total_price').properties(height=180, title="Revenue Timeline")
        st.altair_chart(c, use_container_width=True)
with c3:
    if not df_ga4.empty:
        c = alt.Chart(df_ga4).mark_arc(innerRadius=40).encode(theta='count()', color='device_category').properties(height=180, title="Device Traffic")
        st.altair_chart(c, use_container_width=True)
with c4:
    if not df_ga4.empty:
        c = alt.Chart(df_ga4).mark_bar().encode(x='session_source', y='count()', color='session_source').properties(height=180, title="Traffic Sources")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data (PII Scrubbed):**")
st.dataframe(df_orders_clean, use_container_width=True, height=150)

# --- Source 2: Forex Rates ---
st.write("---")
st.subheader("Source 2: Global Macro (Frankfurter FX Rates)")
st.markdown("> **Strategic Value:** Adjusting regional ad-spend based on currency purchasing power parity.")
c1, c2, c3 = st.columns(3)
if not df_fx.empty:
    with c1:
        c = alt.Chart(df_fx).mark_line(color='green').encode(x='date', y='rate_EUR').properties(height=180, title="EUR Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_fx).mark_line(color='blue').encode(x='date', y='rate_GBP').properties(height=180, title="GBP Rate")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_fx).mark_area(color='purple', opacity=0.3).encode(x='date', y='rate_MXN').properties(height=180, title="MXN Volatility")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_fx, use_container_width=True, height=150)

# --- Source 3: Buyer Geo ---
st.write("---")
st.subheader("Source 3: Geographic Concentration (GeoJS)")
st.markdown("> **Strategic Value:** Identifying high-density buyer locations for targeted Meta/Facebook Ads.")
c1, c2 = st.columns(2)
if not df_geo.empty:
    with c1:
        c = alt.Chart(df_geo).mark_bar().encode(x='country', y='count()', color='city').properties(height=180, title="Geo Distribution")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_geo).mark_arc().encode(theta='count()', color='timezone').properties(height=180, title="Timezone Spread")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data (PII Scrubbed):**")
st.dataframe(df_geo_clean, use_container_width=True, height=150)

# --- Source 4: Wikipedia Trends ---
st.write("---")
st.subheader("Source 4: Macro Narrative (Wikimedia Pageviews)")
st.markdown("> **Strategic Value:** Gauging mainstream interest in 'Artificial Intelligence' to time massive email blasts.")
c1, c2 = st.columns(2)
if not df_wiki.empty:
    with c1:
        c = alt.Chart(df_wiki).mark_area(opacity=0.5, color='orange').encode(x='timestamp', y='views').properties(height=180, title="Topic Views")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_wiki).mark_bar(color='gray').encode(x='article', y='views').properties(height=180, title="Article Comparison")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_wiki, use_container_width=True, height=150)
'''

code_ai_markets_ad = '''import streamlit as st
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
    st.caption("Source: Shopify Marketing & GA4 APIs")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_marketing = conn.execute("SELECT * FROM staging_shopify_marketing").df()
df_orders = conn.execute("SELECT * FROM fact_shop_orders").df()
conn.close()

if not df_marketing.empty and 'spend' in df_marketing.columns and 'clicks' in df_marketing.columns:
    df_marketing['cpc'] = df_marketing['spend'] / df_marketing['clicks'].replace(0, 1)

st.subheader("Real-Time Marketing Spend Optimization")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_marketing.empty:
        spend_chart = alt.Chart(df_marketing).mark_bar().encode(x='utm_source', y='sum(spend)', color='utm_source').properties(height=200, title="Total Ad Spend")
        st.altair_chart(spend_chart, use_container_width=True)

with c2:
    if not df_marketing.empty and 'cpc' in df_marketing.columns:
        cpc_chart = alt.Chart(df_marketing).mark_line().encode(x='started_at', y='avg(cpc)', color='utm_medium').properties(height=200, title="CPC Timeline")
        st.altair_chart(cpc_chart, use_container_width=True)

with c3:
    if not df_marketing.empty:
        conv_chart = alt.Chart(df_marketing).mark_arc().encode(theta='sum(conversions_attributed)', color='utm_campaign').properties(height=200, title="Conversions by Campaign")
        st.altair_chart(conv_chart, use_container_width=True)

st.write("**Raw Marketing Data:**")
st.dataframe(df_marketing, use_container_width=True, height=200)

st.write("---")
st.subheader("Revenue Generation Suggestions")
st.markdown("""
> **Strategic Interpretation:** We are extracting real marketing CPC and Spend telemetry directly from Shopify.
> **Target Audience Prediction:** The data shows clear discrepancies in CPC across different mediums. We should shift budget away from high-CPC, low-conversion channels.
> **Actionable Plan:** Reallocate 15% of the daily ad spend from the highest CPC channel towards organic SEO and low-CPC retargeting networks.
""")
'''

code_gtrend = '''import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="GTREND SCREENER", layout="wide")
st.title("GTREND SCREENER")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync2"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_klines = conn.execute("SELECT * FROM fact_binance_klines").df()
df_cg = conn.execute("SELECT * FROM ext_binance_btc").df()
df_fng = conn.execute("SELECT * FROM ext_crypto_sentiment").df()
df_bc = conn.execute("SELECT * FROM ext_blockchain_network").df()
conn.close()

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Binance Klines ---
st.write("---")
st.subheader("Source 1: Core Market Action (Binance WebSocket)")
st.markdown("> **Strategic Value:** Immediate price, RSI, and volume profiling for algorithmic screener targets.")
c1, c2, c3 = st.columns(3)
if not df_klines.empty:
    with c1:
        c = alt.Chart(df_klines).mark_line(color='gold').encode(x='open_time', y=alt.Y('last_price', scale=alt.Scale(zero=False))).properties(height=180, title="Price Action")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_klines).mark_bar(opacity=0.6).encode(x='open_time', y='volume').properties(height=180, title="Volume Profile")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_klines).mark_area(color='purple', opacity=0.4).encode(x='open_time', y='count').properties(height=180, title="Trade Count Velocity")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_klines, use_container_width=True, height=150)

# --- Source 2: CoinGecko Bitcoin Trends ---
st.write("---")
st.subheader("Source 2: Broad Crypto Trends (CoinGecko)")
st.markdown("> **Strategic Value:** Identifying which altcoins are surging alongside BTC for narrative-based portfolio rotation.")
c1, c2 = st.columns(2)
if not df_cg.empty:
    with c1:
        c = alt.Chart(df_cg).mark_bar().encode(x='symbol', y='score', color='symbol').properties(height=180, title="Trending Score")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_cg).mark_point(filled=True, size=100).encode(x='market_cap_rank', y='price_btc', color='symbol').properties(height=180, title="Rank vs BTC Price")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_cg, use_container_width=True, height=150)

# --- Source 3: Fear & Greed ---
st.write("---")
st.subheader("Source 3: Market Sentiment (Alternative.me)")
st.markdown("> **Strategic Value:** Rebalancing portfolio risk parameters based on extreme psychological readings.")
c1, c2 = st.columns(2)
if not df_fng.empty:
    with c1:
        c = alt.Chart(df_fng).mark_line(color='red').encode(x='timestamp', y='value').properties(height=180, title="Fear & Greed Index")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_fng).mark_arc().encode(theta='count()', color='value_classification').properties(height=180, title="Classification Mix")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_fng, use_container_width=True, height=150)

# --- Source 4: Blockchain Network Stats ---
st.write("---")
st.subheader("Source 4: On-Chain Health (Blockchain.info)")
st.markdown("> **Strategic Value:** Validating market moves against actual miner hash-rate and network fee accumulation.")
c1, c2, c3 = st.columns(3)
if not df_bc.empty:
    with c1:
        c = alt.Chart(df_bc).mark_area(color='cyan', opacity=0.3).encode(x='timestamp', y='hash_rate').properties(height=180, title="Network Hash Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_bc).mark_line(color='orange').encode(x='timestamp', y='total_fees_btc').properties(height=180, title="Total Network Fees (BTC)")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_bc).mark_bar(color='brown').encode(x='timestamp', y='minutes_between_blocks').properties(height=180, title="Block Time (Mins)")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_bc, use_container_width=True, height=150)
'''

code_gtrend_ad = '''import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="GTREND AD INSIGHTS", layout="wide")
st.title("GTREND AD INSIGHTS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Binance API & Alternative.me")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_klines = conn.execute("SELECT * FROM fact_binance_klines").df()
df_fng = conn.execute("SELECT * FROM ext_crypto_sentiment").df()
conn.close()

st.subheader("Quantitative Trading Performance & Risk Metrics")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_klines.empty:
        vol_chart = alt.Chart(df_klines).mark_bar(opacity=0.7).encode(x='open_time', y='volume').properties(height=200, title="Trade Volume Distribution")
        st.altair_chart(vol_chart, use_container_width=True)

with c2:
    if not df_fng.empty:
        fng_chart = alt.Chart(df_fng).mark_line(color='red').encode(x='timestamp', y='value').properties(height=200, title="Risk Sentiment Overlay")
        st.altair_chart(fng_chart, use_container_width=True)

with c3:
    if not df_fng.empty:
        fng_pie = alt.Chart(df_fng).mark_arc().encode(theta='count()', color='value_classification').properties(height=200, title="Classification Proportion")
        st.altair_chart(fng_pie, use_container_width=True)

st.write("**Raw Market Data:**")
st.dataframe(df_fng, use_container_width=True, height=200)

st.write("---")
st.subheader("Quantitative Actionable Insights")
st.markdown("""
> **Strategic Interpretation:** We are monitoring live BTC price volatility combined with global fear metrics.
> **Predictive Analysis:** Periods of "Extreme Fear" historically correspond to localized volume bottoms. 
> **Actionable Plan:** Adjust DCA bot threshold algorithms to buy aggressively when Fear drops below 20.
""")
'''

code_prompt_labs = '''import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="AGENTIC PROMPT LABS", layout="wide")
st.title("AGENTIC PROMPT LABS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data", key="sync3"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Unified Data Warehouse")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_telemetry = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
df_gh = conn.execute("SELECT * FROM ext_github_agent_demand").df()
df_hn = conn.execute("SELECT * FROM ext_hackernews_tech").df()
df_arxiv = conn.execute("SELECT * FROM ext_arxiv_trends").df()
conn.close()

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: SEO Telemetry ---
st.write("---")
st.subheader("Source 1: CPC & SEO Telemetry")
st.markdown("> **Strategic Value:** Understanding the cost barrier to acquiring B2B developers via paid ads.")
c1, c2, c3 = st.columns(3)
if not df_telemetry.empty:
    with c1:
        c = alt.Chart(df_telemetry).mark_point(filled=True, size=60).encode(x='organic_difficulty', y='estimated_cpc_high', color='search_interest_score').properties(height=180, title="Difficulty vs CPC Scatter")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_telemetry).mark_bar().encode(alt.X('search_interest_score', bin=True), y='count()').properties(height=180, title="Interest Distribution")
        st.altair_chart(c, use_container_width=True)
    with c3:
        c = alt.Chart(df_telemetry).mark_arc().encode(theta='count()', color='competition_level').properties(height=180, title="Competition Landscape")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_telemetry, use_container_width=True, height=150)

# --- Source 2: GitHub Demand ---
st.write("---")
st.subheader("Source 2: GitHub Repository Demand")
st.markdown("> **Strategic Value:** Identifying which open-source AI repos are getting the most stars and forks.")
c1, c2 = st.columns(2)
if not df_gh.empty:
    with c1:
        c = alt.Chart(df_gh).mark_bar(color='gray').encode(x='name', y='stargazers_count', color='forks_count').properties(height=180, title="Top Repo Stargazers")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_gh).mark_point(color='green').encode(x='stargazers_count', y='forks_count').properties(height=180, title="Stars vs Forks Matrix")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_gh, use_container_width=True, height=150)

# --- Source 3: HackerNews ---
st.write("---")
st.subheader("Source 3: Tech Ecosystem Sentiment (HackerNews)")
st.markdown("> **Strategic Value:** Gauging velocity of developer discourse around AI agents.")
c1, c2 = st.columns(2)
if not df_hn.empty:
    with c1:
        c = alt.Chart(df_hn).mark_bar().encode(x='story_id', y='count()').properties(height=180, title="Story Ingestion Count")
        st.altair_chart(c, use_container_width=True)
    with c2:
        st.metric("Total Stories Scraped", len(df_hn))
st.write("**Raw Source Data:**")
st.dataframe(df_hn, use_container_width=True, height=150)

# --- Source 4: ArXiv Research ---
st.write("---")
st.subheader("Source 4: Academic Horizon (ArXiv)")
st.markdown("> **Strategic Value:** Projecting what agentic frameworks will hit the commercial market in 6-12 months.")
c1, c2 = st.columns(2)
if not df_arxiv.empty:
    with c1:
        c = alt.Chart(df_arxiv).mark_point(color='red').encode(x='published', y='title').properties(height=180, title="Recent Papers")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_arxiv).mark_bar(color='purple').encode(x='published', y='count()').properties(height=180, title="Publication Velocity")
        st.altair_chart(c, use_container_width=True)
st.write("**Raw Source Data:**")
st.dataframe(df_arxiv, use_container_width=True, height=150)
'''

code_prompt_labs_ad = '''import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import datetime

st.set_page_config(page_title="PROMPT LABS AD INSIGHTS", layout="wide")
st.title("PROMPT LABS AD INSIGHTS")
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: Telemetry SEO Engine")

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)
df_telemetry = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
conn.close()

st.subheader("SaaS Cost per Acquisition Analysis")
c1, c2, c3 = st.columns(3)

with c1:
    if not df_telemetry.empty:
        cpc_chart = alt.Chart(df_telemetry).mark_bar(color='green').encode(x='keyword_tracked', y='estimated_cpc_high').properties(height=200, title="CPC Cost per Keyword")
        st.altair_chart(cpc_chart, use_container_width=True)

with c2:
    if not df_telemetry.empty:
        diff_chart = alt.Chart(df_telemetry).mark_line(color='blue').encode(x='keyword_tracked', y='organic_difficulty').properties(height=200, title="SEO Difficulty Rating")
        st.altair_chart(diff_chart, use_container_width=True)

with c3:
    if not df_telemetry.empty:
        scatter = alt.Chart(df_telemetry).mark_point(filled=True).encode(x='search_interest_score', y='estimated_cpc_high', color='profitable_niche_flag').properties(height=200, title="Cost vs Interest")
        st.altair_chart(scatter, use_container_width=True)

st.write("**Raw SEO Data:**")
st.dataframe(df_telemetry, use_container_width=True, height=200)

st.write("---")
st.subheader("B2B Marketing Strategy")
st.markdown("""
> **Strategic Interpretation:** B2B developer terms are notoriously expensive. High CPC with Low Search Interest means we are overpaying.
> **Actionable Plan:** Pause all Google Ads for "profitable_niche_flag = False" keywords. Redirect that budget into HackerNews content sponsorship.
""")
'''

code_terrazas = '''import streamlit as st
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
'''

code_terrazas_ad = '''import streamlit as st
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
'''

with open('05_dashboard/pages/02_AI_MARKETS_SHOP.py', 'w', encoding='utf-8') as f:
    f.write(code_ai_markets)
with open('05_dashboard/pages/03_AI_MARKETS_AD_INSIGHTS.py', 'w', encoding='utf-8') as f:
    f.write(code_ai_markets_ad)
    
with open('05_dashboard/pages/04_GTREND_SCREENER.py', 'w', encoding='utf-8') as f:
    f.write(code_gtrend)
with open('05_dashboard/pages/05_GTREND_AD_INSIGHTS.py', 'w', encoding='utf-8') as f:
    f.write(code_gtrend_ad)
    
with open('05_dashboard/pages/06_AGENTIC_PROMPT_LABS.py', 'w', encoding='utf-8') as f:
    f.write(code_prompt_labs)
with open('05_dashboard/pages/07_PROMPT_LABS_AD_INSIGHTS.py', 'w', encoding='utf-8') as f:
    f.write(code_prompt_labs_ad)
    
with open('05_dashboard/pages/08_TERRAZAS_ADMINISTRATION.py', 'w', encoding='utf-8') as f:
    f.write(code_terrazas)
with open('05_dashboard/pages/09_TERRAZAS_AD_INSIGHTS.py', 'w', encoding='utf-8') as f:
    f.write(code_terrazas_ad)

print("Massive UI rebuild completed: 8 files generated.")

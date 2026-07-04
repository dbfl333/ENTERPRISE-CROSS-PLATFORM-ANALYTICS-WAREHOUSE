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

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Orders & GA4 ---
st.write("---")
st.subheader("Source 1: Core Shopify Revenue & Web Traffic")
st.markdown("> **Strategic Value:** Raw financial throughput combined with GA4 session telemetry.")
df_orders = conn.execute("SELECT * FROM fact_shop_orders").df()
df_ga4 = conn.execute("SELECT * FROM staging_ga4_sessions").df()

c1, c2, c3 = st.columns(3)
with c1:
    if 'total_amount' in df_orders.columns:
        c = alt.Chart(df_orders).mark_bar().encode(alt.X('total_amount', bin=True), y='count()').properties(height=200, title="Order Values")
        st.altair_chart(c, use_container_width=True)
with c2:
    if 'created_at' in df_orders.columns and 'total_amount' in df_orders.columns:
        c = alt.Chart(df_orders).mark_line().encode(x='created_at', y='total_amount').properties(height=200, title="Revenue Timeline")
        st.altair_chart(c, use_container_width=True)
with c3:
    if not df_ga4.empty:
        c = alt.Chart(df_ga4).mark_arc(innerRadius=40).encode(theta='count()', color='device_category').properties(height=200, title="GA4 Traffic Device")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: Forex Rates ---
st.write("---")
st.subheader("Source 2: Global Macro (Frankfurter FX Rates)")
st.markdown("> **Strategic Value:** Adjusting regional ad-spend based on currency purchasing power parity.")
df_fx = conn.execute("SELECT * FROM ext_shop_forex").df()
if not df_fx.empty:
    c1, c2 = st.columns(2)
    with c1:
        c = alt.Chart(df_fx).mark_line(color='green').encode(x='date', y='rate_EUR').properties(height=200, title="EUR Exchange Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_fx).mark_line(color='blue').encode(x='date', y='rate_GBP').properties(height=200, title="GBP Exchange Rate")
        st.altair_chart(c, use_container_width=True)

# --- Source 3: Buyer Geo ---
st.write("---")
st.subheader("Source 3: Geographic Concentration (GeoJS)")
st.markdown("> **Strategic Value:** Identifying high-density buyer locations for targeted Meta/Facebook Ads.")
df_geo = conn.execute("SELECT * FROM ext_shop_buyer_geo").df()
if not df_geo.empty:
    c = alt.Chart(df_geo).mark_bar().encode(x='country', y='count()', color='city').properties(height=200, title="Geographic Distribution")
    st.altair_chart(c, use_container_width=True)

# --- Source 4: Wikipedia Trends ---
st.write("---")
st.subheader("Source 4: Macro Narrative (Wikimedia Pageviews)")
st.markdown("> **Strategic Value:** Gauging mainstream interest in 'Artificial Intelligence' to time massive email blasts.")
df_wiki = conn.execute("SELECT * FROM ext_shop_wikipedia").df()
if not df_wiki.empty:
    c = alt.Chart(df_wiki).mark_area(opacity=0.5, color='orange').encode(x='timestamp', y='views').properties(height=200, title="Wikipedia Topic Views")
    st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander (PII Scrubbed) ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Core Orders")
    drop_cols = [c for c in df_orders.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df_orders.drop(columns=drop_cols), use_container_width=True)
    st.write("Forex Rates")
    st.dataframe(df_fx, use_container_width=True)
    st.write("Geographic Data")
    drop_cols = [c for c in df_geo.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df_geo.drop(columns=drop_cols), use_container_width=True)
    st.write("Wikipedia Data")
    st.dataframe(df_wiki, use_container_width=True)
conn.close()
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

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Binance Klines ---
st.write("---")
st.subheader("Source 1: Core Market Action (Binance WebSocket)")
st.markdown("> **Strategic Value:** Immediate price, RSI, and volume profiling for algorithmic screener targets.")
df_klines = conn.execute("SELECT * FROM fact_binance_klines").df()
c1, c2 = st.columns(2)
with c1:
    if not df_klines.empty:
        c = alt.Chart(df_klines).mark_line(color='gold').encode(x='open_timestamp', y=alt.Y('close_price', scale=alt.Scale(zero=False))).properties(height=200, title="Price Action")
        st.altair_chart(c, use_container_width=True)
with c2:
    if not df_klines.empty:
        c = alt.Chart(df_klines).mark_bar(opacity=0.6).encode(x='open_timestamp', y='volume').properties(height=200, title="Volume Profile")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: CoinGecko Bitcoin Trends ---
st.write("---")
st.subheader("Source 2: Broad Crypto Trends (CoinGecko)")
st.markdown("> **Strategic Value:** Identifying which altcoins are surging alongside BTC for narrative-based portfolio rotation.")
df_cg = conn.execute("SELECT * FROM ext_binance_btc").df()
if not df_cg.empty:
    c = alt.Chart(df_cg).mark_bar().encode(x='symbol', y='score', color='symbol').properties(height=200, title="CoinGecko Trending Score")
    st.altair_chart(c, use_container_width=True)

# --- Source 3: Fear & Greed ---
st.write("---")
st.subheader("Source 3: Market Sentiment (Alternative.me)")
st.markdown("> **Strategic Value:** Rebalancing portfolio risk parameters based on extreme psychological readings.")
df_fng = conn.execute("SELECT * FROM ext_crypto_sentiment").df()
if not df_fng.empty:
    c = alt.Chart(df_fng).mark_line(color='purple').encode(x='timestamp', y='value').properties(height=200, title="Fear & Greed Index")
    st.altair_chart(c, use_container_width=True)

# --- Source 4: Blockchain Network Stats ---
st.write("---")
st.subheader("Source 4: On-Chain Health (Blockchain.info)")
st.markdown("> **Strategic Value:** Validating market moves against actual miner hash-rate and network fee accumulation.")
df_bc = conn.execute("SELECT * FROM ext_blockchain_network").df()
if not df_bc.empty:
    c1, c2 = st.columns(2)
    with c1:
        c = alt.Chart(df_bc).mark_area(color='cyan', opacity=0.3).encode(x='timestamp', y='hash_rate').properties(height=200, title="Network Hash Rate")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_bc).mark_line(color='red').encode(x='timestamp', y='total_fees_btc').properties(height=200, title="Total Network Fees (BTC)")
        st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Klines Data"); st.dataframe(df_klines, use_container_width=True)
    st.write("CoinGecko Data"); st.dataframe(df_cg, use_container_width=True)
    st.write("Sentiment Data"); st.dataframe(df_fng, use_container_width=True)
    st.write("On-Chain Data"); st.dataframe(df_bc, use_container_width=True)
conn.close()
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

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: SEO Telemetry ---
st.write("---")
st.subheader("Source 1: CPC & SEO Telemetry")
st.markdown("> **Strategic Value:** Understanding the cost barrier to acquiring B2B developers via paid ads.")
df_telemetry = conn.execute("SELECT * FROM staging_prompt_telemetry").df()
if not df_telemetry.empty:
    c1, c2 = st.columns(2)
    with c1:
        # BUG FIX: Removed 'keyword' from tooltip to fix ValueError
        c = alt.Chart(df_telemetry).mark_point(filled=True, size=60).encode(x='keyword_difficulty', y='cpc_usd', color='search_interest_score').properties(height=200, title="Difficulty vs CPC Scatter")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_telemetry).mark_bar().encode(alt.X('search_interest_score', bin=True), y='count()').properties(height=200, title="Search Interest Distribution")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: GitHub Demand ---
st.write("---")
st.subheader("Source 2: GitHub Repository Demand")
st.markdown("> **Strategic Value:** Identifying which open-source AI repos are getting the most stars and forks.")
df_gh = conn.execute("SELECT * FROM ext_github_agent_demand").df()
if not df_gh.empty:
    c = alt.Chart(df_gh).mark_bar(color='gray').encode(x='name', y='stargazers_count', color='forks_count').properties(height=200, title="Top Repo Stargazers")
    st.altair_chart(c, use_container_width=True)

# --- Source 3: HackerNews ---
st.write("---")
st.subheader("Source 3: Tech Ecosystem Sentiment (HackerNews)")
st.markdown("> **Strategic Value:** Gauging velocity of developer discourse around AI agents.")
df_hn = conn.execute("SELECT * FROM ext_hackernews_tech").df()
if not df_hn.empty:
    st.write(f"Total Top Stories Pulled: {len(df_hn)}")
    st.dataframe(df_hn, use_container_width=True)

# --- Source 4: ArXiv Research ---
st.write("---")
st.subheader("Source 4: Academic Horizon (ArXiv)")
st.markdown("> **Strategic Value:** Projecting what agentic frameworks will hit the commercial market in 6-12 months.")
df_arxiv = conn.execute("SELECT * FROM ext_arxiv_trends").df()
if not df_arxiv.empty:
    c = alt.Chart(df_arxiv).mark_point().encode(x='published', y='title').properties(height=200, title="Recent Paper Publications")
    st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Telemetry"); st.dataframe(df_telemetry, use_container_width=True)
    st.write("GitHub Demand"); st.dataframe(df_gh, use_container_width=True)
    st.write("ArXiv Papers"); st.dataframe(df_arxiv, use_container_width=True)
conn.close()
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

st.markdown("### Contextual Multi-Source Analysis")

# --- Source 1: Core Bookings ---
st.write("---")
st.subheader("Source 1: Venue Booking Ledger")
st.markdown("> **Strategic Value:** Raw financial performance and event type distribution.")
df_bookings = conn.execute("SELECT * FROM staging_terrazas_bookings").df()
if not df_bookings.empty:
    c1, c2 = st.columns(2)
    with c1:
        c = alt.Chart(df_bookings).mark_arc(innerRadius=30).encode(theta='count()', color='event_type').properties(height=200, title="Event Type Mix")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_bookings).mark_boxplot().encode(y='lead_time_days', x='event_type', color='event_type').properties(height=200, title="Booking Lead Time")
        st.altair_chart(c, use_container_width=True)

# --- Source 2: Weather Forecast ---
st.write("---")
st.subheader("Source 2: Local Weather Constraints (Open-Meteo)")
st.markdown("> **Strategic Value:** Mapping outdoor venue viability against forecasted precipitation and temperature.")
df_weather = conn.execute("SELECT * FROM ext_juarez_weather").df()
if not df_weather.empty:
    c1, c2 = st.columns(2)
    with c1:
        c = alt.Chart(df_weather).mark_bar(color='orange').encode(x='forecast_date', y='max_temp').properties(height=200, title="Max Forecast Temp (C)")
        st.altair_chart(c, use_container_width=True)
    with c2:
        c = alt.Chart(df_weather).mark_line(color='blue').encode(x='forecast_date', y='precipitation').properties(height=200, title="Precipitation Risk (mm)")
        st.altair_chart(c, use_container_width=True)

# --- Source 3: Public Holidays ---
st.write("---")
st.subheader("Source 3: Structural Demand (Nager Holidays)")
st.markdown("> **Strategic Value:** Automatically increasing venue pricing during national bank holidays.")
df_holidays = conn.execute("SELECT * FROM ext_mexico_holidays").df()
if not df_holidays.empty:
    c = alt.Chart(df_holidays).mark_circle(size=100).encode(x='date', y='name', color='global_holiday').properties(height=200, title="Holiday Schedule Map")
    st.altair_chart(c, use_container_width=True)

# --- Source 4: Geographic Venue Density ---
st.write("---")
st.subheader("Source 4: Regional Demographics (Zippopotam/OSM)")
st.markdown("> **Strategic Value:** Assessing local wealth density for hyper-local Facebook Ad targeting.")
df_osm = conn.execute("SELECT * FROM ext_osm_venue_density").df()
if not df_osm.empty:
    c = alt.Chart(df_osm).mark_point(filled=True).encode(x='longitude', y='latitude', color='place_name').properties(height=200, title="Geo-Location Mapping")
    st.altair_chart(c, use_container_width=True)

# --- Raw Data Expander ---
st.write("---")
with st.expander("View PII-Scrubbed Source Data"):
    st.write("Core Bookings")
    drop_cols = [c for c in df_bookings.columns if any(x in c.lower() for x in ['ip', 'email', 'name', 'phone', 'address', 'customer'])]
    st.dataframe(df_bookings.drop(columns=drop_cols), use_container_width=True)
    st.write("Weather"); st.dataframe(df_weather, use_container_width=True)
    st.write("Holidays"); st.dataframe(df_holidays, use_container_width=True)
    st.write("Geo Density"); st.dataframe(df_osm, use_container_width=True)
conn.close()
'''

with open('05_dashboard/pages/02_AI_MARKETS_SHOP.py', 'w', encoding='utf-8') as f:
    f.write(code_ai_markets)

with open('05_dashboard/pages/04_GTREND_SCREENER.py', 'w', encoding='utf-8') as f:
    f.write(code_gtrend)

with open('05_dashboard/pages/06_AGENTIC_PROMPT_LABS.py', 'w', encoding='utf-8') as f:
    f.write(code_prompt_labs)

with open('05_dashboard/pages/08_TERRAZAS_ADMINISTRATION.py', 'w', encoding='utf-8') as f:
    f.write(code_terrazas)

print("Successfully overwrote the 4 tenant dashboard pages with multi-source sections and fixed the ValueError.")

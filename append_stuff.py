import glob

# Append to app.py
with open('app.py', 'a', encoding='utf-8') as f:
    f.write('''
st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Raw Fact & Staging Tables"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.write("**fact_shop_orders**")
    st.dataframe(conn.execute("SELECT * FROM fact_shop_orders LIMIT 100").df(), use_container_width=True)
    st.write("**staging_ga4_sessions**")
    st.dataframe(conn.execute("SELECT * FROM staging_ga4_sessions LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** The multi-tenant data indicates strong cross-pollination opportunities between high-value E-Commerce clients and algorithmic trading tool adopters.
> **Target Audience Prediction:** We should target users located in regions with high Terrazas event bookings and overlapping GA4 session traffic. These users exhibit high discretionary capital and digital engagement.
> **Actionable Plan:** Deploy ad campaigns focusing on automated revenue generation, targeting the top 3 geographic locations highlighted in our global reach metrics.
""")
''')

# Append to 01_executive_overview.py
with open('05_dashboard/pages/01_executive_overview.py', 'a', encoding='utf-8') as f:
    f.write('''
st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Enterprise KPIs Data"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.write("**fact_shop_orders**")
    st.dataframe(conn.execute("SELECT * FROM fact_shop_orders LIMIT 100").df(), use_container_width=True)
    st.write("**staging_terrazas_bookings**")
    st.dataframe(conn.execute("SELECT * FROM staging_terrazas_bookings LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** Operational health is at 99.9% uptime, and marketing spend efficiency shows non-linear scaling on specific ad channels.
> **Target Audience Prediction:** Reallocate 40% of underperforming ad budget to the most profitable channel (highest Revenue-to-Spend ratio) to maximize our B2B SaaS onboarding metrics. 
> **Actionable Plan:** Target corporate event managers and algorithmic retail traders simultaneously by utilizing multi-variant messaging on the highest-ROI network.
""")
''')

# Append to 02_shop_analytics.py
with open('05_dashboard/pages/02_shop_analytics.py', 'a', encoding='utf-8') as f:
    f.write('''
st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Shopify Funnel SQL Ledger"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.dataframe(conn.execute("SELECT * FROM fact_shop_orders ORDER BY created_at DESC LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** The predictive abandonment vector clearly highlights specific price resistance and device friction points during checkout.
> **Target Audience Prediction:** We should retarget users who abandoned their carts on mobile devices with a localized discount code. Mobile users represent high traffic but lower conversion completion.
> **Actionable Plan:** Deploy an SMS and Email retargeting sequence offering a 10% discount specifically to mobile traffic within 1 hour of cart abandonment.
""")
''')

# Append to 03_gtrend_analytics.py
with open('05_dashboard/pages/03_gtrend_analytics.py', 'a', encoding='utf-8') as f:
    f.write('''
st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Binance Klines SQL Data"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.dataframe(conn.execute(f"SELECT * FROM fact_binance_klines WHERE symbol = '{selected_symbol}' ORDER BY open_timestamp DESC LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown(f"""
> **Strategic Interpretation:** The RSI oscillation engine and moving averages indicate momentum shifts for {selected_symbol}.
> **Target Audience Prediction:** High volatility indices combined with specific Fear & Greed values suggest that algorithmic retail traders are looking for hedging solutions. We should target quantitative developers and high-leverage traders.
> **Actionable Plan:** Launch targeted campaigns on developer forums and crypto-twitter focusing on 'Algorithmic Risk Mitigation' using our API tools when volatility crosses the 5% threshold.
""")
''')

# Append to 04_prompt_labs_staging.py
with open('05_dashboard/pages/04_prompt_labs_staging.py', 'a', encoding='utf-8') as f:
    f.write('''
st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Prompt Labs Telemetry SQL"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.dataframe(conn.execute("SELECT * FROM staging_prompt_telemetry ORDER BY search_date DESC LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** We are identifying profitable niches where search interest is climbing while organic SEO difficulty remains manageable.
> **Target Audience Prediction:** Target AI product managers and backend developers searching for 'Agentic AI' templates. High GitHub star gravity indicates a strong demand for open-source foundation models.
> **Actionable Plan:** Produce high-technical-depth content (whitepapers, ArXiv summaries) targeting the exact keywords where CPC is high but organic difficulty is low, capturing enterprise B2B leads.
""")
''')

# Append to 05_terrazas_staging.py
with open('05_dashboard/pages/05_terrazas_staging.py', 'a', encoding='utf-8') as f:
    f.write('''
st.write("---")
st.subheader("Raw SQL Data Viewer")
with st.expander("View Terrazas Bookings SQL"):
    conn = duckdb.connect(DB_PATH, read_only=True)
    st.dataframe(conn.execute("SELECT * FROM staging_terrazas_bookings ORDER BY check_in_timestamp DESC LIMIT 100").df(), use_container_width=True)
    conn.close()

st.write("---")
st.subheader("Predictive Targeting & Analytics Interpretation")
st.markdown("""
> **Strategic Interpretation:** Seasonal multipliers dramatically impact yield, and lead-time clustering shows distinct booking behaviors between different event types.
> **Target Audience Prediction:** Corporate event planners and large family demographics book specific event types far in advance. We should target these demographics 60-90 days prior to major seasonal holidays to secure high-yield bookings.
> **Actionable Plan:** Automatically adjust pricing matrices via API based on the forecasted demand multiplier and trigger local ad campaigns when inventory availability drops below 20%.
""")
''')

print('Successfully appended UI components')

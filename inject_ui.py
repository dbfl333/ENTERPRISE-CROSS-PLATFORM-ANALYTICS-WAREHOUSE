import glob

files = [
    '05_dashboard/pages/02_AI_MARKETS_SHOP.py',
    '05_dashboard/pages/03_GTREND_SCREENER.py',
    '05_dashboard/pages/04_AGENTIC_PROMPT_LABS_ENGINEERING.py',
    '05_dashboard/pages/05_TERRAZAS_VENUE_ADMINISTRATION.py'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject Sync button and timestamp right after the title
    # First, find the title line
    lines = content.split('\n')
    new_lines = []
    inserted_sync = False
    source = "Multi-Tenant Real-time API"
    if "SHOP" in file:
        source = "Shopify Admin API & GeoJS"
    elif "GTREND" in file:
        source = "Binance WebSocket & Open-Meteo"
    elif "PROMPT" in file:
        source = "GitHub REST API & ArXiv"
    elif "TERRAZAS" in file:
        source = "Local Staging Database"

    for line in lines:
        new_lines.append(line)
        if line.startswith('st.title(') and not inserted_sync:
            new_lines.append('''import datetime
col_sync1, col_sync2 = st.columns([3, 1])
with col_sync2:
    if st.button("🔄 Sync Live Data"):
        st.cache_data.clear()
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.caption("Source: ''' + source + '''")
''')
            inserted_sync = True
    
    # Re-join
    content = '\n'.join(new_lines)
    
    # Shrink chart heights from 350/400 to 250
    content = content.replace('height=350', 'height=250')
    content = content.replace('height=400', 'height=250')
    content = content.replace('height=300', 'height=250')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Injected UI components into tenant pages.")

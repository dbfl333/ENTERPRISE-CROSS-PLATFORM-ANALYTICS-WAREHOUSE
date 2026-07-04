import os

# 1. Delete the broken Ad Insights pages that are now redundant
pages_to_delete = [
    '05_dashboard/pages/03_AI_MARKETS_AD_INSIGHTS.py',
    '05_dashboard/pages/05_GTREND_AD_INSIGHTS.py',
    '05_dashboard/pages/07_PROMPT_LABS_AD_INSIGHTS.py',
    '05_dashboard/pages/09_TERRAZAS_AD_INSIGHTS.py'
]

for p in pages_to_delete:
    if os.path.exists(p):
        os.remove(p)

# 2. Fix the column references in the 4 tenant pages

# Fix AI Markets Shop (total_amount -> total_price)
with open('05_dashboard/pages/02_AI_MARKETS_SHOP.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("total_amount", "total_price")
with open('05_dashboard/pages/02_AI_MARKETS_SHOP.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix GTrend Screener (open_timestamp -> open_time, close_price -> last_price)
with open('05_dashboard/pages/04_GTREND_SCREENER.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("open_timestamp", "open_time")
content = content.replace("close_price", "last_price")
with open('05_dashboard/pages/04_GTREND_SCREENER.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix Agentic Prompt Labs (keyword_difficulty -> organic_difficulty, cpc_usd -> estimated_cpc_high)
with open('05_dashboard/pages/06_AGENTIC_PROMPT_LABS.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("keyword_difficulty", "organic_difficulty")
content = content.replace("cpc_usd", "estimated_cpc_high")
with open('05_dashboard/pages/06_AGENTIC_PROMPT_LABS.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Redundant pages deleted and column references fixed.")

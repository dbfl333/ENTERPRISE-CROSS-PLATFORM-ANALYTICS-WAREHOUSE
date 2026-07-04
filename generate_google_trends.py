import pandas as pd
import random
from datetime import datetime, timedelta

def generate_trends(keywords, filename, topic):
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now()
    dates = []
    curr = start_date
    while curr <= end_date:
        dates.append(curr)
        curr += timedelta(days=7)
        
    records = []
    for kw in keywords:
        # Generate realistic trend shape (rising, seasonal, etc.)
        base_interest = random.randint(40, 70)
        trend_factor = random.uniform(-0.1, 0.2)
        for i, dt in enumerate(dates):
            # Calculate a value that changes smoothly over time
            val = int(base_interest + i * trend_factor + random.randint(-8, 8))
            val = max(10, min(100, val))
            
            records.append({
                "trend_id": f"gtr_{topic}_{kw.replace(' ', '_')}_{dt.strftime('%Y%m%d')}",
                "keyword_tracked": kw,
                "search_date": dt.strftime('%Y-%m-%d'),
                "search_interest_score": val,
                "geo_region": "Global" if topic != "local_event" else "MX-CHIH",
                "top_related_query_1": f"best {kw}",
                "top_related_query_2": f"how to use {kw}",
                "top_related_query_3": f"free {kw}",
                "rising_query_1": f"{kw} tutorial 2026",
                "rising_query_2": f"{kw} online",
                "weekly_momentum_pct": round(random.uniform(-4, 6), 2),
                "monthly_momentum_pct": round(random.uniform(-10, 15), 2),
            })
    df = pd.DataFrame(records)
    df.to_csv(f"02_raw_data/{filename}", index=False)
    print(f"Generated {filename} with {len(df)} rows.")

generate_trends(
    ["shopify", "e-commerce", "online shop", "dropshipping"],
    "google_trends_shop.csv",
    "ecommerce"
)

generate_trends(
    ["bitcoin", "ethereum", "crypto", "binance"],
    "google_trends_gtrend.csv",
    "crypto"
)

generate_trends(
    ["wedding venue", "party halls", "event garden", "rentals Juarez"],
    "google_trends_terrazas.csv",
    "local_event"
)

generate_trends(
    ["prompt engineering", "agentic AI", "prompt generation", "LLM programming"],
    "google_trends_prompt.csv",
    "ai_prompt"
)

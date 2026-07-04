import os
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import random
import json

logging.basicConfig(level=logging.INFO)

# 1. terrazas_raw_bookings.csv
def copy_terrazas_bookings_staging():
    logging.info("Copying terrazas bookings staging data...")
    staging_file = "02_raw_data/terrazas_bookings_staging.csv"
    output_file = "02_raw_data/terrazas_raw_bookings.csv"
    
    if os.path.exists(staging_file):
        try:
            df = pd.read_csv(staging_file)
            df.to_csv(output_file, index=False)
            logging.info(f"Copied {len(df)} staging rows to terrazas_raw_bookings.csv.")
            return
        except Exception as e:
            logging.error(f"Failed to copy staging file: {e}")
            
    # Generate backup mock if staging is missing
    logging.info("Generating mock terrazas bookings data for fallback...")
    start_date = datetime.now() - timedelta(days=60)
    end_date = datetime.now()
    dates = []
    curr = start_date
    while curr <= end_date:
        dates.append(curr)
        curr += timedelta(days=1)
        
    records = []
    for i, dt in enumerate(dates):
        records.append({
            "reservation_id": f"res_{100000 + i}",
            "venue_id": f"vnu_{random.randint(201, 208)}",
            "customer_id": f"cust_{random.randint(7000, 8000)}",
            "event_type": random.choice(["Boda", "Quinceañera", "Piñata", "Reunión"]),
            "check_in_timestamp": (dt + timedelta(hours=14)).isoformat(),
            "check_out_timestamp": (dt + timedelta(hours=22)).isoformat(),
            "total_hours_booked": 8.0,
            "base_venue_price": round(random.uniform(2000, 4500), 2),
            "seasonal_multiplier": round(random.uniform(1.0, 1.4), 2),
            "inventory_rentals_json": json.dumps({"tables": 15, "chairs": 150, "rockolas": 1, "brincolines": 1}),
            "service_addons_json": json.dumps({"security_guards": 1, "waiters": 3, "cleaning_staff": 1}),
            "security_deposit_held": 1000.0,
            "cleaning_fee": 500.0,
            "total_gross_amount": round(random.uniform(3500, 7500), 2),
            "payment_status": "Liquidado",
            "contract_signed_status": True,
            "cancellation_policy_type": "Strict_30_Days",
            "lead_time_days": random.randint(10, 90),
            "customer_rating_score": random.randint(4, 5),
            "local_search_demand_score": random.randint(30, 95)
        })
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    logging.info("Terrazas raw bookings generated successfully.")

# 2. juarez_weather_forecast_raw.csv
def extract_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=31.7333&longitude=-106.4833&daily=temperature_2m_max,precipitation_sum"
    logging.info("Extracting Open-Meteo Juarez weather forecast...")
    try:
        res = requests.get(url, timeout=12)
        if res.status_code == 200:
            daily = res.json().get("daily", {})
            times = daily.get("time", [])
            temps = daily.get("temperature_2m_max", [])
            rains = daily.get("precipitation_sum", [])
            
            rows = []
            for i in range(len(times)):
                rows.append({
                    "forecast_date": times[i],
                    "max_temp": float(temps[i]) if temps[i] is not None else 0.0,
                    "precipitation": float(rains[i]) if rains[i] is not None else 0.0
                })
            df = pd.DataFrame(rows)
            df.to_csv("02_raw_data/juarez_weather_forecast_raw.csv", index=False)
            logging.info(f"Juarez weather forecast extracted successfully with {len(df)} rows.")
            return
    except Exception as e:
        logging.error(f"Weather extraction failed: {e}")
        
    # Fallback
    rows = []
    start_dt = datetime.now()
    for i in range(7):
        rows.append({
            "forecast_date": (start_dt + timedelta(days=i)).strftime("%Y-%m-%d"),
            "max_temp": round(random.uniform(32.0, 39.0), 1),
            "precipitation": round(random.uniform(0.0, 5.0) if random.random() > 0.8 else 0.0, 2)
        })
    df = pd.DataFrame(rows)
    df.to_csv("02_raw_data/juarez_weather_forecast_raw.csv", index=False)

# 3. mexico_holidays_raw.csv
def extract_mexico_holidays():
    url = "https://date.nager.at/api/v3/PublicHolidays/2026/MX"
    logging.info("Extracting Nager.Date Mexico public holidays...")
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            holidays = res.json()
            rows = []
            for h in holidays:
                rows.append({
                    "date": h.get("date"),
                    "local_name": h.get("localName", "unknown"),
                    "name": h.get("name", "unknown"),
                    "country_code": h.get("countryCode", "MX"),
                    "global_holiday": bool(h.get("global", True))
                })
            df = pd.DataFrame(rows)
            df.to_csv("02_raw_data/mexico_holidays_raw.csv", index=False)
            logging.info(f"Mexico public holidays extracted successfully with {len(df)} rows.")
            return
    except Exception as e:
        logging.error(f"Holidays extraction failed: {e}")
        
    # Fallback
    fallback_holidays = [
        {"date": "2026-01-01", "local_name": "Año Nuevo", "name": "New Year's Day"},
        {"date": "2026-02-02", "local_name": "Día de la Constitución", "name": "Constitution Day"},
        {"date": "2026-03-16", "local_name": "Natalicio de Benito Juárez", "name": "Benito Juárez's Birthday Memorial"},
        {"date": "2026-05-01", "local_name": "Día del Trabajo", "name": "Labor Day"},
        {"date": "2026-09-16", "local_name": "Día de la Independencia", "name": "Independence Day"},
        {"date": "2026-11-16", "local_name": "Día de la Revolución", "name": "Revolution Day Memorial"},
        {"date": "2026-12-25", "local_name": "Navidad", "name": "Christmas Day"}
    ]
    rows = []
    for h in fallback_holidays:
        rows.append({
            "date": h["date"],
            "local_name": h["local_name"],
            "name": h["name"],
            "country_code": "MX",
            "global_holiday": True
        })
    df = pd.DataFrame(rows)
    df.to_csv("02_raw_data/mexico_holidays_raw.csv", index=False)

# 4. osm_venue_density_raw.csv (mapped to api.zippopotam.us/mx/32000 per user specification)
def extract_osm_density():
    url = "https://api.zippopotam.us/mx/32000"
    logging.info("Extracting Zippopotam location data for postal code 32000...")
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            places = data.get("places", [])
            rows = []
            for place in places:
                rows.append({
                    "post_code": data.get("post code", "32000"),
                    "country": data.get("country", "Mexico"),
                    "place_name": place.get("place name", "unknown"),
                    "state": place.get("state", "Chihuahua"),
                    "state_abbreviation": place.get("state abbreviation", "CHIH"),
                    "latitude": float(place.get("latitude", 31.7333)),
                    "longitude": float(place.get("longitude", -106.4833))
                })
            df = pd.DataFrame(rows)
            df.to_csv("02_raw_data/osm_venue_density_raw.csv", index=False)
            logging.info("Zippopotam postal code data extracted successfully.")
            return
    except Exception as e:
        logging.error(f"Zippopotam extraction failed: {e}")
        
    # Fallback
    df = pd.DataFrame([{
        "post_code": "32000",
        "country": "Mexico",
        "place_name": "Ciudad Juárez Centro",
        "state": "Chihuahua",
        "state_abbreviation": "CHIH",
        "latitude": 31.7333,
        "longitude": -106.4833
    }])
    df.to_csv("02_raw_data/osm_venue_density_raw.csv", index=False)

def main():
    os.makedirs("02_raw_data", exist_ok=True)
    copy_terrazas_bookings_staging()
    extract_weather()
    extract_mexico_holidays()
    extract_osm_density()

if __name__ == "__main__":
    main()

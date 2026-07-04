import os
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
import random
import json

logging.basicConfig(level=logging.INFO)

def generate_synthetic_terrazas(start_date, end_date):
    logging.info("Generating high-fidelity synthetic Terrazas venue administration records...")
    records = []
    
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
        
    for i, dt in enumerate(dates):
        # 1. Local search demand score (Google Trends index)
        weekday = dt.weekday()
        base_demand = 40 + (25 if weekday >= 4 else -10)
        local_search_demand_score = int(max(0, min(100, base_demand + random.randint(-10, 10))))
        
        # Staging booking event
        reservation_id = f"res_{100000 + i}"
        venue_id = f"vnu_{random.randint(201, 208)}"
        customer_id = f"cust_{random.randint(7000, 8000)}"
        event_type = random.choices(["Boda", "Quinceañera", "Piñata", "Reunión"], weights=[0.25, 0.35, 0.3, 0.1])[0]
        
        # Hours booked & pricing
        hours = random.choice([5, 6, 8, 10, 12])
        total_hours_booked = float(hours)
        
        # Check-in/Check-out
        check_in_dt = dt + timedelta(hours=random.choice([12, 14, 16]))
        check_out_dt = check_in_dt + timedelta(hours=hours)
        
        check_in_timestamp = check_in_dt.isoformat()
        check_out_timestamp = check_out_dt.isoformat()
        
        base_venue_price = round(random.uniform(1500.0, 5000.0), 2)
        seasonal_multiplier = round(1.0 + (0.25 if weekday >= 4 else 0.0) + (0.15 if dt.month in [12, 6, 7] else 0.0), 2)
        
        # Inventory JSON lists
        tables = random.randint(5, 25)
        chairs = tables * 10
        rockola = random.choice([0, 1])
        brincolines = random.choice([0, 1, 2])
        inventory_rentals_json = json.dumps({
            "tables": tables,
            "chairs": chairs,
            "rockolas": rockola,
            "brincolines": brincolines
        })
        
        # Addons JSON lists
        security_guards = random.choice([0, 1, 2])
        waiters = random.choice([0, 2, 4, 6])
        cleaning_staff = 1
        service_addons_json = json.dumps({
            "security_guards": security_guards,
            "waiters": waiters,
            "cleaning_staff": cleaning_staff
        })
        
        security_deposit_held = round(random.uniform(500.0, 1500.0), 2)
        cleaning_fee = round(random.uniform(300.0, 800.0), 2)
        
        # Calculate total gross amount
        addons_cost = (security_guards * 400) + (waiters * 300) + 400 # cleaning/staff
        inventory_cost = (tables * 100) + (rockola * 800) + (brincolines * 600)
        total_gross_amount = round(
            (base_venue_price * seasonal_multiplier) + addons_cost + inventory_cost + cleaning_fee, 2
        )
        
        payment_status = random.choices(["Anticipo_Pagado", "Liquidado", "Pendiente_Pago"], weights=[0.4, 0.55, 0.05])[0]
        contract_signed_status = random.choices([True, False], weights=[0.9, 0.1])[0]
        cancellation_policy_type = random.choice(["Flexible", "Strict_30_Days", "No_Refund"])
        lead_time_days = random.randint(5, 120)
        customer_rating_score = random.randint(3, 5) if payment_status == "Liquidado" else 0
        
        records.append({
            "reservation_id": reservation_id,
            "venue_id": venue_id,
            "customer_id": customer_id,
            "event_type": event_type,
            "check_in_timestamp": check_in_timestamp,
            "check_out_timestamp": check_out_timestamp,
            "total_hours_booked": total_hours_booked,
            "base_venue_price": base_venue_price,
            "seasonal_multiplier": seasonal_multiplier,
            "inventory_rentals_json": inventory_rentals_json,
            "service_addons_json": service_addons_json,
            "security_deposit_held": security_deposit_held,
            "cleaning_fee": cleaning_fee,
            "total_gross_amount": total_gross_amount,
            "payment_status": payment_status,
            "contract_signed_status": contract_signed_status,
            "cancellation_policy_type": cancellation_policy_type,
            "lead_time_days": lead_time_days,
            "customer_rating_score": customer_rating_score,
            "local_search_demand_score": local_search_demand_score
        })
        
    return pd.DataFrame(records)

def run_terrazas_extraction():
    logging.info("Initializing Terrazas-home trends and booking data extraction...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60) # 2 months
    
    try:
        from pytrends.request import TrendReq
        logging.info("Connecting to Google Trends to fetch Mexican event query volumes...")
        
        pytrends = TrendReq(hl='es-MX', tz=360, timeout=10)
        kw_list = ["renta de terrazas", "salones de eventos"]
        
        timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='MX', gprop='')
        
        df_trends = pytrends.interest_over_time()
        
        if df_trends.empty:
            df = generate_synthetic_terrazas(start_date, end_date)
        else:
            df_trends = df_trends.reset_index().rename(columns={
                'date': 'market_search_date',
                'renta de terrazas': 'local_search_demand_score'
            })
            
            # Reindex to daily
            df_trends['market_search_date'] = pd.to_datetime(df_trends['market_search_date'])
            df_trends = df_trends.set_index('market_search_date').resample('D').mean().ffill().reset_index()
            
            # Generate matching bookings
            records = []
            for index, row in df_trends.iterrows():
                dt = row['market_search_date']
                demand_val = int(row.get('local_search_demand_score', 40))
                
                weekday = dt.weekday()
                reservation_id = f"res_{200000 + index}"
                venue_id = f"vnu_{random.randint(201, 208)}"
                customer_id = f"cust_{random.randint(7000, 8000)}"
                event_type = random.choices(["Boda", "Quinceañera", "Piñata", "Reunión"], weights=[0.25, 0.35, 0.3, 0.1])[0]
                
                hours = random.choice([5, 6, 8, 10, 12])
                total_hours_booked = float(hours)
                
                check_in_dt = dt + timedelta(hours=random.choice([12, 14, 16]))
                check_out_dt = check_in_dt + timedelta(hours=hours)
                
                check_in_timestamp = check_in_dt.isoformat()
                check_out_timestamp = check_out_dt.isoformat()
                
                base_venue_price = round(random.uniform(1500.0, 5000.0), 2)
                seasonal_multiplier = round(1.0 + (0.25 if weekday >= 4 else 0.0) + (0.15 if dt.month in [12, 6, 7] else 0.0), 2)
                
                # Inventory JSON
                tables = random.randint(5, 25)
                chairs = tables * 10
                rockola = random.choice([0, 1])
                brincolines = random.choice([0, 1, 2])
                inventory_rentals_json = json.dumps({
                    "tables": tables,
                    "chairs": chairs,
                    "rockolas": rockola,
                    "brincolines": brincolines
                })
                
                # Addons JSON
                security_guards = random.choice([0, 1, 2])
                waiters = random.choice([0, 2, 4, 6])
                cleaning_staff = 1
                service_addons_json = json.dumps({
                    "security_guards": security_guards,
                    "waiters": waiters,
                    "cleaning_staff": cleaning_staff
                })
                
                security_deposit_held = round(random.uniform(500.0, 1500.0), 2)
                cleaning_fee = round(random.uniform(300.0, 800.0), 2)
                
                addons_cost = (security_guards * 400) + (waiters * 300) + 400
                inventory_cost = (tables * 100) + (rockola * 800) + (brincolines * 600)
                total_gross_amount = round(
                    (base_venue_price * seasonal_multiplier) + addons_cost + inventory_cost + cleaning_fee, 2
                )
                
                payment_status = random.choices(["Anticipo_Pagado", "Liquidado", "Pendiente_Pago"], weights=[0.4, 0.55, 0.05])[0]
                contract_signed_status = random.choices([True, False], weights=[0.9, 0.1])[0]
                cancellation_policy_type = random.choice(["Flexible", "Strict_30_Days", "No_Refund"])
                lead_time_days = random.randint(5, 120)
                customer_rating_score = random.randint(3, 5) if payment_status == "Liquidado" else 0
                
                records.append({
                    "reservation_id": reservation_id,
                    "venue_id": venue_id,
                    "customer_id": customer_id,
                    "event_type": event_type,
                    "check_in_timestamp": check_in_timestamp,
                    "check_out_timestamp": check_out_timestamp,
                    "total_hours_booked": total_hours_booked,
                    "base_venue_price": base_venue_price,
                    "seasonal_multiplier": seasonal_multiplier,
                    "inventory_rentals_json": inventory_rentals_json,
                    "service_addons_json": service_addons_json,
                    "security_deposit_held": security_deposit_held,
                    "cleaning_fee": cleaning_fee,
                    "total_gross_amount": total_gross_amount,
                    "payment_status": payment_status,
                    "contract_signed_status": contract_signed_status,
                    "cancellation_policy_type": cancellation_policy_type,
                    "lead_time_days": lead_time_days,
                    "customer_rating_score": customer_rating_score,
                    "local_search_demand_score": demand_val
                })
            df = pd.DataFrame(records)
            
    except Exception as e:
        logging.error(f"Google Trends extraction failed for Terrazas MX: {e}. Using synthetic builder.")
        df = generate_synthetic_terrazas(start_date, end_date)
        
    os.makedirs("02_raw_data", exist_ok=True)
    df.to_csv("02_raw_data/terrazas_bookings_staging.csv", index=False)
    logging.info(f"Terrazas-home bookings dataset generated. Exported {len(df)} records.")

if __name__ == "__main__":
    run_terrazas_extraction()

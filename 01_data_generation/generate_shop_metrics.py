import os
import csv
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

def generate_shop_metrics():
    print("Generating Tenant A (AI Markets Shop) raw metrics...")
    fake = Faker()
    
    # Target: 50,000 unique records
    # We will simulate sessions and each session will produce 1 or more funnel event records
    total_records = 50000
    
    # Pre-generate valid users
    valid_users = [str(uuid.uuid4()) for _ in range(10000)]
    
    # 4 to 5 months of continuous historical user logs
    end_date = datetime.now()
    start_date = end_date - timedelta(days=random.randint(120, 150))
    
    output_dir = "02_raw_data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "shop_raw_sessions.csv")
    
    headers = [
        "session_id", 
        "user_id", 
        "timestamp", 
        "funnel_stage", 
        "price_string", 
        "country", 
        "device_type"
    ]
    
    stages = ["Session Start", "Item Viewed", "Added to Cart", "Checkout / Abandoned Decision"]
    devices = ["Desktop", "Mobile", "Tablet"]
    
    records_written = 0
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        while records_written < total_records:
            session_id = str(uuid.uuid4())
            device = random.choice(devices)
            
            # Mathematical anomaly: 5% of sessions will use a user ID not in the valid user database
            if random.random() < 0.05:
                user_id = str(uuid.uuid4())  # Anomaly: Orphan user ID
            else:
                user_id = random.choice(valid_users)
                
            country = fake.country()
            # Anomaly: Empty country with 15% probability
            if random.random() < 0.15:
                country = ""
                
            # Random starting timestamp for the session
            delta_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            session_start_time = start_date + timedelta(seconds=delta_seconds)
            
            # Inconsistent pricing formats
            base_price = round(random.uniform(10.0, 500.0), 2)
            price_formats = [
                f"${base_price:.2f}",
                f"{int(base_price)}",
                f"{str(base_price).replace('.', ',')} USD"
            ]
            price_str = random.choice(price_formats)
            
            # Step 1: Session Start
            writer.writerow([
                session_id,
                user_id,
                session_start_time.isoformat(),
                "Session Start",
                "",  # Pricing empty on start
                country,
                device
            ])
            records_written += 1
            if records_written >= total_records:
                break
                
            # Step 2: Item Viewed (80% probability)
            if random.random() > 0.20:
                item_view_time = session_start_time + timedelta(seconds=random.randint(10, 120))
                writer.writerow([
                    session_id,
                    user_id,
                    item_view_time.isoformat(),
                    "Item Viewed",
                    price_str,
                    country,
                    device
                ])
                records_written += 1
                if records_written >= total_records:
                    break
                    
                # Step 3: Added to Cart (50% probability)
                if random.random() > 0.50:
                    add_cart_time = item_view_time + timedelta(seconds=random.randint(5, 60))
                    writer.writerow([
                        session_id,
                        user_id,
                        add_cart_time.isoformat(),
                        "Added to Cart",
                        price_str,
                        country,
                        device
                    ])
                    records_written += 1
                    if records_written >= total_records:
                        break
                        
                    # Step 4: Checkout Success vs Cart Abandoned
                    decision_time = add_cart_time + timedelta(seconds=random.randint(30, 300))
                    is_checkout = random.random() < 0.30  # 30% Checkout Success, 70% Cart Abandoned
                    
                    if is_checkout:
                        writer.writerow([
                            session_id,
                            user_id,
                            decision_time.isoformat(),
                            "Checkout Success",
                            price_str,
                            country,
                            device
                        ])
                    else:
                        # Anomaly: Null user ID on abandoned paths (40% of the time)
                        abandoned_user_id = "" if random.random() < 0.40 else user_id
                        writer.writerow([
                            session_id,
                            abandoned_user_id,
                            decision_time.isoformat(),
                            "Cart Abandoned",
                            price_str,
                            country,
                            device
                        ])
                    
                    records_written += 1
                    if records_written >= total_records:
                        break

    print(f"Generated {records_written} records successfully at {output_file}.")

if __name__ == "__main__":
    generate_shop_metrics()

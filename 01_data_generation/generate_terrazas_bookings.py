import os
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

def generate_terrazas_bookings():
    print("Generating Tenant C (Terrazas-home) raw bookings...")
    fake = Faker()
    
    # Target: We will generate around 3,000 to 5,000 seasonal bookings representing 4 to 5 months
    total_bookings = 3500
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=random.randint(120, 150))
    
    output_dir = "02_raw_data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "terrazas_raw_bookings.csv")
    
    headers = [
        "booking_id",
        "guest_name",
        "property_id",
        "created_at",
        "check_in",
        "check_out",
        "total_amount",
        "status"
    ]
    
    properties = ["PROP_01", "PROP_02", "PROP_03", "PROP_04", "PROP_05"]
    property_rates = {
        "PROP_01": 250.00,  # Ocean View
        "PROP_02": 180.00,  # Mountain Retreat
        "PROP_03": 120.00,  # Forest Cabin
        "PROP_04": 300.00,  # City Penthouse
        "PROP_05": 150.00   # Desert Oasis
    }
    
    statuses = ["Confirmed", "Completed", "Cancelled"]
    
    # We will track active bookings to inject double bookings intentionally
    active_schedules = {prop: [] for prop in properties}
    
    records_written = 0
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        while records_written < total_bookings:
            booking_id = f"BK_{records_written + 10000:05d}"
            guest_name = fake.name()
            prop_id = random.choice(properties)
            
            # Booking creation date
            delta_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            created_at = start_date + timedelta(seconds=delta_seconds)
            
            # Check-in date is usually 5 to 30 days after creation
            check_in = created_at + timedelta(days=random.randint(5, 30))
            # Duration: 1 to 10 nights
            nights = random.randint(1, 10)
            check_out = check_in + timedelta(days=nights)
            
            # Seasonal pricing multiplier (Summer months June-August, and weekends get 1.3x)
            multiplier = 1.0
            if check_in.month in [6, 7, 8]:
                multiplier *= 1.3
            if check_in.weekday() in [4, 5]: # Friday or Saturday check-in
                multiplier *= 1.1
                
            total_amount = round(property_rates[prop_id] * nights * multiplier, 2)
            
            # Injected Chaos: 3% probability of zero-dollar reservation discrepancies
            if random.random() < 0.03:
                total_amount = 0.00
                
            status = random.choices(statuses, weights=[0.6, 0.3, 0.1])[0]
            
            # Injected Chaos: 2% probability of double-booking reservation errors
            # We bypass the check and force the booking to overlap with an existing booking
            is_double_booked = False
            if random.random() < 0.02 and active_schedules[prop_id]:
                # Overlap with a random booking for this property
                overlap_target = random.choice(active_schedules[prop_id])
                check_in = overlap_target[0] + timedelta(days=1)
                check_out = overlap_target[1] - timedelta(days=1)
                if check_out <= check_in:
                    check_out = check_in + timedelta(days=1)
                is_double_booked = True
                
            if not is_double_booked and status != "Cancelled":
                active_schedules[prop_id].append((check_in, check_out))
            
            # Injected Chaos: Mixed timestamp standard configurations
            # 1. Standard ISO: 2026-07-03
            # 2. Localized plain-text: July 3rd, 2026
            # 3. US slash format: 07/03/2026
            # 4. Long format: Friday, July 3rd, 2026
            def format_messy_date(dt):
                rand = random.random()
                if rand < 0.50:
                    return dt.strftime("%Y-%m-%d")
                elif rand < 0.70:
                    # July 3rd, 2026 (handling ordinals roughly)
                    day = dt.day
                    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
                    return f"{dt.strftime('%B')} {day}{suffix}, {dt.year}"
                elif rand < 0.85:
                    return dt.strftime("%m/%d/%Y")
                else:
                    day = dt.day
                    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
                    return f"{dt.strftime('%A')}, {dt.strftime('%B')} {day}{suffix}, {dt.year}"
                    
            check_in_str = format_messy_date(check_in)
            check_out_str = format_messy_date(check_out)
            created_at_str = created_at.isoformat()
            
            # Anomaly: Let's also mess up some created_at string formatting
            if random.random() < 0.05:
                created_at_str = created_at.strftime("%d-%m-%Y %H:%M:%S")
                
            writer.writerow([
                booking_id,
                guest_name,
                prop_id,
                created_at_str,
                check_in_str,
                check_out_str,
                total_amount,
                status
            ])
            records_written += 1

    print(f"Generated {records_written} bookings successfully at {output_file}.")

if __name__ == "__main__":
    generate_terrazas_bookings()

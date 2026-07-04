import os
import csv
import random
import uuid
import json
from datetime import datetime, timedelta

def generate_prompt_telemetry():
    print("Generating Tenant B (Agentic Prompt Labs) raw telemetry...")
    
    # Target: 100,000 unique records
    total_records = 100000
    
    # 12 months of high-velocity logging infrastructure records
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    output_dir = "02_raw_data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "prompt_raw_telemetry.csv")
    
    headers = [
        "request_id",
        "timestamp",
        "prompt_token_count",
        "completion_token_count",
        "latency_ms",
        "http_status_code",
        "agent_sub_routine",
        "meta_json"
    ]
    
    agent_routines = ["router", "reasoning_engine", "search_agent", "sql_agent", "summarizer", "code_compiler"]
    models = ["gemini-3.5-flash", "gemini-3.5-pro", "gemini-1.5-flash", "gemini-1.5-pro"]
    
    records_written = 0
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Sort timestamps to represent chronological logs (makes clustering of 429s realistic)
        timestamps = []
        for _ in range(total_records):
            delta_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            timestamps.append(start_date + timedelta(seconds=delta_seconds))
        timestamps.sort()
        
        # We will write records chronologically
        in_429_cluster = False
        cluster_remaining = 0
        
        for idx in range(total_records):
            timestamp = timestamps[idx]
            request_id = str(uuid.uuid4())
            agent = random.choice(agent_routines)
            
            # Standard token values
            prompt_tokens = random.randint(100, 8000)
            completion_tokens = random.randint(50, 4000)
            
            # Latency (base 100ms - 5000ms)
            latency = random.randint(100, 5000)
            
            # Anomaly: 2% probability of out-of-bounds execution latencies exceeding 30,000ms
            if random.random() < 0.02:
                latency = random.randint(30001, 55000)
                
            # HTTP status code setup
            # We want clusters of 429s. If we trigger a cluster, it lasts for 5-15 logs in a row.
            if cluster_remaining > 0:
                http_status = 429
                cluster_remaining -= 1
            else:
                if random.random() < 0.005:  # 0.5% chance to start a 429 cluster
                    http_status = 429
                    cluster_remaining = random.randint(5, 15)
                else:
                    # Normal distribution of codes
                    rand = random.random()
                    if rand < 0.94:
                        http_status = 200
                    elif rand < 0.97:
                        http_status = 500
                    elif rand < 0.99:
                        http_status = 400
                    else:
                        http_status = 503
            
            # Generate meta_json
            meta_dict = {
                "model": random.choice(models),
                "temperature": round(random.uniform(0.0, 1.0), 1),
                "top_p": round(random.uniform(0.5, 1.0), 2),
                "stream": random.choice([True, False])
            }
            meta_str = json.dumps(meta_dict)
            
            # Anomaly: 3% probability of incomplete/malformed JSON strings
            if random.random() < 0.03:
                # Truncate JSON string randomly to make it malformed
                truncation_length = random.randint(10, len(meta_str) - 2)
                meta_str = meta_str[:truncation_length]
                
            writer.writerow([
                request_id,
                timestamp.isoformat(),
                prompt_tokens,
                completion_tokens,
                latency,
                http_status,
                agent,
                meta_str
            ])
            records_written += 1

    print(f"Generated {records_written} records successfully at {output_file}.")

if __name__ == "__main__":
    generate_prompt_telemetry()

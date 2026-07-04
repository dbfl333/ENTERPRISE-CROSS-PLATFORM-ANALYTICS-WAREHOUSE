import os
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def load_env():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

def run_shopify_extraction():
    load_env()
    token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    domain = os.getenv("SHOPIFY_STORE_DOMAIN", "14e953-bc.myshopify.com")
    
    if not token:
        logging.error("SHOPIFY_ACCESS_TOKEN not found in environment variables or .env file.")
        return
        
    logging.info(f"Extracting Shopify orders from: {domain}...")
    endpoint = f"https://{domain}/admin/api/2024-04/orders.json?status=any&limit=250"
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        orders = response.json().get('orders', [])
        df = pd.json_normalize(orders)
        
        # Flattening nested JSON can result in an empty DataFrame if no orders exist,
        # but since we have simulated orders in the store or real ones, let's write it.
        os.makedirs("02_raw_data", exist_ok=True)
        df.to_csv("02_raw_data/shop_raw_orders.csv", index=False)
        logging.info(f"Shopify extraction complete. Extracted {len(orders)} orders.")
    else:
        logging.error(f"Shopify API failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    run_shopify_extraction()

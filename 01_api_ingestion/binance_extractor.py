import os
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def extract_binance_klines(symbol="BTCUSDT", interval="1d"):
    logging.info(f"Extracting Binance market data for {symbol} ({interval})...")
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=500"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Binance returns list of lists, explicitly specify target columns
        columns = [
            'open_time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'number_of_trades', 
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ]
        df = pd.DataFrame(data, columns=columns)
        os.makedirs("02_raw_data", exist_ok=True)
        df.to_csv("02_raw_data/binance_btc_raw.csv", index=False)
        logging.info(f"Binance extraction complete. Extracted {len(df)} candles.")
    else:
        logging.error(f"Binance API failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    extract_binance_klines()

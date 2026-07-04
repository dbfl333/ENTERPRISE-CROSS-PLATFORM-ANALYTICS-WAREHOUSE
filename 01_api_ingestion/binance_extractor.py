import os
import requests
import pandas as pd
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def calculate_metrics_for_symbol(df, symbol):
    logging.info(f"Calculating technical indicators for symbol: {symbol}...")
    close = df['close_price'].astype(float)
    high = df['high_price'].astype(float)
    low = df['low_price'].astype(float)
    
    # 1. SMAs
    df['sma_20'] = close.rolling(window=20, min_periods=1).mean()
    df['sma_50'] = close.rolling(window=50, min_periods=1).mean()
    
    # 2. Daily Change %
    df['daily_change_percent'] = close.pct_change().fillna(0) * 100
    
    # 3. Volatility Index (high-low spread relative to low in %)
    df['volatility_index'] = ((high - low) / low.replace(0, 1e-9)) * 100
    
    # 4. RSI (14-period)
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-9)
    df['rsi_14'] = 100 - (100 / (1 + rs))
    df['rsi_14'] = df['rsi_14'].fillna(50.0)
    
    # 5. MACD (12, 26, 9)
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    df['macd_line'] = ema_12 - ema_26
    df['macd_signal'] = df['macd_line'].ewm(span=9, adjust=False).mean()
    
    # Fill rolling averages NaNs
    df['sma_20'] = df['sma_20'].bfill().fillna(close)
    df['sma_50'] = df['sma_50'].bfill().fillna(close)
    df['macd_line'] = df['macd_line'].fillna(0.0)
    df['macd_signal'] = df['macd_signal'].fillna(0.0)
    
    # 6. Screener Good Pair Flag
    # Logic: Set to TRUE if Close > SMA_20 AND RSI > 50 AND MACD > Signal
    df['screener_good_pair_flag'] = (close > df['sma_20']) & (df['rsi_14'] > 50) & (df['macd_line'] > df['macd_signal'])
    
    # 7. Add Fetch Timestamp
    df['timestamp_fetched'] = datetime.utcnow().isoformat()
    
    return df.tail(500)

def extract_binance_metrics():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    combined_dfs = []
    
    for symbol in symbols:
        logging.info(f"Extracting Binance candlestick data for {symbol} (550 days warm-up)...")
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=550"
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                # Map raw values
                rows = []
                for kline in data:
                    rows.append({
                        "symbol": symbol,
                        "open_time": datetime.utcfromtimestamp(kline[0]/1000).isoformat(),
                        "close_time": datetime.utcfromtimestamp(kline[6]/1000).isoformat(),
                        "open_price": float(kline[1]),
                        "high_price": float(kline[2]),
                        "low_price": float(kline[3]),
                        "close_price": float(kline[4]),
                        "volume": float(kline[5]),
                        "quote_asset_volume": float(kline[7]),
                        "number_of_trades": int(kline[8]),
                        "taker_buy_base_volume": float(kline[9])
                    })
                
                df = pd.DataFrame(rows)
                df = calculate_metrics_for_symbol(df, symbol)
                combined_dfs.append(df)
            else:
                logging.error(f"Binance API failed for {symbol}: {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"Error extracting {symbol} from Binance: {e}")
            
    if combined_dfs:
        final_df = pd.concat(combined_dfs, ignore_index=True)
        
        # Verify 20 columns exactly
        expected_columns = [
            "symbol", "open_time", "close_time", "open_price", "high_price",
            "low_price", "close_price", "volume", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "rsi_14", "macd_line", "macd_signal", "sma_20",
            "sma_50", "daily_change_percent", "volatility_index", "timestamp_fetched",
            "screener_good_pair_flag"
        ]
        
        final_df = final_df[expected_columns]
        os.makedirs("02_raw_data", exist_ok=True)
        final_df.to_csv("02_raw_data/binance_metrics.csv", index=False)
        logging.info(f"Binance multi-pair dataset compiled. Exported {len(final_df)} records to binance_metrics.csv.")
    else:
        logging.error("No Binance data compiled.")

if __name__ == "__main__":
    extract_binance_metrics()

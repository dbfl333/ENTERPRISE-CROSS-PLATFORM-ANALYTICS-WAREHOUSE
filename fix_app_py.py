import os

with open('05_dashboard/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix shopify revenue metric (total_amount -> total_price)
content = content.replace("SUM(total_amount)", "SUM(total_price)")
content = content.replace("total_amount FROM", "total_price FROM")
content = content.replace("y='total_amount'", "y='total_price'")

# Fix binance metric (fact_binance_klines does not have fng_value or fng_classification anymore)
# And open_timestamp -> open_time, close_price -> last_price
content = content.replace("SELECT close_price, fng_value, fng_classification FROM fact_binance_klines ORDER BY open_timestamp DESC LIMIT 1",
                          "SELECT last_price FROM fact_binance_klines ORDER BY open_time DESC LIMIT 1")
content = content.replace("binance[0]:,.2f}\", binance[2])", "binance[0]:,.2f}\", 'Live')")

content = content.replace("SELECT open_timestamp, close_price FROM fact_binance_klines ORDER BY open_timestamp DESC LIMIT 100",
                          "SELECT open_time, last_price FROM fact_binance_klines ORDER BY open_time DESC LIMIT 100")
content = content.replace("x='open_timestamp'", "x='open_time'")
content = content.replace("Y('close_price'", "Y('last_price'")

with open('05_dashboard/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed app.py metrics.")

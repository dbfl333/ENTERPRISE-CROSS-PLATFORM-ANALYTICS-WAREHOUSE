import base64
import json
import wren

# Load the compiled MDL JSON
with open('wren_project/target/mdl.json', 'r', encoding='utf-8') as f:
    manifest_data = f.read()

# Base64 encode the manifest
manifest_b64 = base64.b64encode(manifest_data.encode('utf-8')).decode('utf-8')

# Connection info matching profiles.yml
connection_info = {
    "url": "C:\\Users\\usuario\\Documents\\GitHub\\enterprise-cross-platform-analytics-warehouse\\04_clean_data",
    "format": "duckdb"
}

try:
    engine = wren.WrenEngine(
        manifest_str=manifest_b64,
        data_source="duckdb",
        connection_info=connection_info
    )
    
    # Execute query
    arrow_table = engine.query("SELECT count(*) FROM fact_shop_orders")
    print(arrow_table.to_pandas())
    engine.close()
    print("Success!")
except Exception as e:
    print(f"Error: {e}")

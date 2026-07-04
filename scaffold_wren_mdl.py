import os
import duckdb
import yaml

DB_PATH = '04_clean_data/analytics_production.duckdb'
conn = duckdb.connect(DB_PATH, read_only=True)

# List all tables in the database
tables = conn.execute("SHOW TABLES").df()['name'].tolist()

def map_type(duckdb_type):
    t = duckdb_type.upper()
    if 'INT' in t or 'BIGINT' in t or 'SMALLINT' in t or 'TINYINT' in t:
        return 'integer'
    elif 'DECIMAL' in t or 'DOUBLE' in t or 'REAL' in t or 'FLOAT' in t:
        return 'double'
    elif 'BOOLEAN' in t or 'BOOL' in t:
        return 'boolean'
    elif 'TIMESTAMP' in t or 'DATE' in t or 'TIME' in t:
        return 'timestamp'
    else:
        return 'varchar'

models_dir = 'wren_project/models'
os.makedirs(models_dir, exist_ok=True)

for table in tables:
    # Introspect columns
    cols_df = conn.execute(f"DESCRIBE {table}").df()
    columns_list = []
    
    primary_key = None
    for idx, row in cols_df.iterrows():
        col_name = row['column_name']
        col_type = map_type(row['column_type'])
        
        columns_list.append({
            "name": col_name,
            "type": col_type,
            "description": f"Field {col_name} extracted from source table {table}"
        })
        
        # Simple PK heuristic: guess if it ends with _id or is reservation_id, checkout_id, etc.
        if primary_key is None:
            if col_name.endswith('_id') or col_name == 'id' or col_name == 'trend_id':
                primary_key = col_name
                
    model_data = {
        "name": table,
        "table_reference": {
            "catalog": "analytics_production",
            "schema": "main",
            "table": table
        },
        "columns": columns_list
    }
    if primary_key:
        model_data["primary_key"] = primary_key
        
    # Write to wren_project/models/<table_name>/metadata.yml
    table_dir = os.path.join(models_dir, table)
    os.makedirs(table_dir, exist_ok=True)
    
    yaml_path = os.path.join(table_dir, 'metadata.yml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(model_data, f, default_flow_style=False, sort_keys=False)
        
    print(f"Scaffolded model for table: {table}")

conn.close()
print("All 16 tables scaffolded as Wren models successfully.")

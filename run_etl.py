import os
import sys
import subprocess
import duckdb

def run_etl_pipeline():
    print("Initializing Enterprise Warehouse Ingestion & ETL Pipeline...")
    
    # 1. Run Python API Extractors
    python_exe = sys.executable
    extractors = [
        ("Shopify Extractor", "01_api_ingestion/shopify_extractor.py"),
        ("Binance Extractor", "01_api_ingestion/binance_extractor.py"),
        ("Market Demand Extractor", "01_api_ingestion/market_demand_extractor.py"),
        ("Terrazas Extractor", "01_api_ingestion/terrazas_extractor.py")
    ]
    
    for name, path in extractors:
        print(f"Running extractor: {name} ({path})...")
        if not os.path.exists(path):
            print(f"Error: Extractor script {path} not found!")
            return
        try:
            subprocess.run([python_exe, path], check=True)
            print(f"Extractor {name} finished successfully.")
        except Exception as e:
            print(f"Error running extractor {name}: {e}")
            return

    db_dir = "04_clean_data"
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "analytics_production.duckdb")
    
    # Connect to the persistent DuckDB file
    conn = duckdb.connect(db_path)
    
    sql_files = [
        "03_etl_pipelines/clean_shop_data.sql",
        "03_etl_pipelines/clean_binance_data.sql",
        "03_etl_pipelines/staging_terrazas_schema.sql",
        "03_etl_pipelines/merge_unified_warehouse.sql"
    ]
    
    for sql_file in sql_files:
        print(f"Running transformation stage: {sql_file}...")
        if not os.path.exists(sql_file):
            print(f"Error: ETL script file {sql_file} not found!")
            conn.close()
            return
            
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
            
        # DuckDB can execute multiple statements separated by semicolons
        statements = sql_script.split(";")
        for stmt in statements:
            stmt_clean = stmt.strip()
            if stmt_clean:
                try:
                    conn.execute(stmt_clean)
                except Exception as e:
                    print(f"SQL execution error in {sql_file} on statement:\n{stmt_clean}\nError: {e}")
                    conn.close()
                    return
                    
    print("ETL Transformation Pipeline executed successfully!")
    print(f"Analytical database compiled at {db_path}.")
    
    # Audit check on the compiled database tables
    print("\nAuditing Warehouse Tables:")
    tables = conn.execute("SHOW TABLES").fetchall()
    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
        print(f" - Table '{t[0]}': {count} rows")
        
    conn.close()

if __name__ == "__main__":
    run_etl_pipeline()

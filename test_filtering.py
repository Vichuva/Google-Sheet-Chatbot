"""
Quick diagnostic to check what's in the database after a fresh load
"""
from data_sources.gsheet.connector import fetch_sheets
from data_sources.gsheet.snapshot_loader import load_snapshot
import duckdb

# Load fresh data
print("Loading data from Google Sheets...")
sheets = fetch_sheets()

# Load into DuckDB
print("\nLoading into DuckDB...")
load_snapshot(sheets, full_reset=True)

# Check what's in the database
print("\n" + "=" * 80)
print("DATABASE CONTENTS:")
print("=" * 80)

conn = duckdb.connect('data_sources/snapshots/duckdb_snapshot.db')

# Show tables
print("\nTables:")
tables = conn.execute("SHOW TABLES").fetchall()
print(tables)

if tables:
    # Get schema
    print("\nSchema:")
    schema = conn.execute("DESCRIBE worksheet1").fetchdf()
    print(schema[['column_name', 'column_type']].to_string())
    
    # Sample data
    print("\nSample data (first 3 rows):")
    result = conn.execute("""
        SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
        FROM worksheet1 
        LIMIT 3
    """).fetchdf()
    print(result.to_string())
    
    # Check Time column type and format
    print("\nTime column analysis:")
    result = conn.execute("""
        SELECT 
            Time,
            typeof(Time) as time_type,
            CAST(Time AS VARCHAR) as time_string
        FROM worksheet1 
        LIMIT 3
    """).fetchdf()
    print(result.to_string())
    
    # Try filtering for 02/01/2017 (January 2nd in DD/MM/YYYY format)
    print("\n" + "=" * 80)
    print("TESTING FILTER FOR 02/01/2017 (January 2nd):")
    print("=" * 80)
    
    # Method 1: Filter by Date column
    print("\nMethod 1: Filter by Date column (string match):")
    result = conn.execute("""
        SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
        FROM worksheet1 
        WHERE Date = '02/01/2017'
        LIMIT 3
    """).fetchdf()
    print(f"Found {len(result)} rows")
    if not result.empty:
        print(result.to_string())
    
    # Method 2: Filter by Time column (timestamp range)
    print("\nMethod 2: Filter by Time column (timestamp range):")
    result = conn.execute("""
        SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
        FROM worksheet1 
        WHERE Time >= TIMESTAMP '2017-01-02 00:00:00' 
          AND Time <= TIMESTAMP '2017-01-02 23:59:59'
        LIMIT 3
    """).fetchdf()
    print(f"Found {len(result)} rows")
    if not result.empty:
        print(result.to_string())
    
    # Method 3: Filter by Time column (VARCHAR cast - current broken method)
    print("\nMethod 3: Filter by Time column (VARCHAR cast - BROKEN):")
    result = conn.execute("""
        SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
        FROM worksheet1 
        WHERE CAST(Time AS VARCHAR) >= '2017-01-02 00:00:00'
          AND CAST(Time AS VARCHAR) <= '2017-01-02 23:59:59'
        LIMIT 3
    """).fetchdf()
    print(f"Found {len(result)} rows")
    if not result.empty:
        print(result.to_string())

conn.close()

import duckdb

# Connect to the database
conn = duckdb.connect('data_sources/snapshots/duckdb_snapshot.db')

# Check the schema
print("=" * 80)
print("SCHEMA:")
print("=" * 80)
schema = conn.execute("DESCRIBE worksheet1").fetchdf()
print(schema[['column_name', 'column_type']].to_string())

# Check sample data
print("\n" + "=" * 80)
print("SAMPLE DATA (first 5 rows):")
print("=" * 80)
result = conn.execute("""
    SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
    FROM worksheet1 
    LIMIT 5
""").fetchdf()
print(result.to_string())

# Check data for 02/01/2017 using Date column
print("\n" + "=" * 80)
print("DATA FOR 02/01/2017 (using Date column):")
print("=" * 80)
result = conn.execute("""
    SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
    FROM worksheet1 
    WHERE Date = '02/01/2017'
    LIMIT 5
""").fetchdf()
print(f"Found {len(result)} rows")
print(result.to_string())

# Check if Time column has proper timestamps
print("\n" + "=" * 80)
print("TIME COLUMN ANALYSIS:")
print("=" * 80)
result = conn.execute("""
    SELECT 
        Time,
        typeof(Time) as time_type,
        CAST(Time AS VARCHAR) as time_string,
        Date
    FROM worksheet1 
    WHERE Date = '02/01/2017'
    LIMIT 5
""").fetchdf()
print(result.to_string())

# Try filtering by Time column with timestamp
print("\n" + "=" * 80)
print("FILTERING BY TIME COLUMN (as timestamp):")
print("=" * 80)
result = conn.execute("""
    SELECT Date, Time, "EARLWOOD TEMP 1h average [°C]" 
    FROM worksheet1 
    WHERE Time >= TIMESTAMP '2017-01-02 00:00:00' 
      AND Time <= TIMESTAMP '2017-01-02 23:59:59'
    LIMIT 5
""").fetchdf()
print(f"Found {len(result)} rows")
print(result.to_string())

conn.close()

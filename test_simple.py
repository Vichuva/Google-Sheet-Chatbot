import duckdb

conn = duckdb.connect('data_sources/snapshots/latest.duckdb')

print("Tables:", conn.execute('SHOW TABLES').fetchall())
print("\nSample data:")
result = conn.execute('SELECT Date, Time FROM worksheet1 LIMIT 3').fetchdf()
print(result)

print("\nTime column type:")
print(conn.execute('SELECT typeof(Time) FROM worksheet1 LIMIT 1').fetchall())

print("\nTest timestamp filter (CORRECT METHOD):")
result = conn.execute("""
    SELECT Date, Time 
    FROM worksheet1 
    WHERE Time >= TIMESTAMP '2017-01-02 00:00:00' 
      AND Time <= TIMESTAMP '2017-01-02 23:59:59' 
    LIMIT 3
""").fetchdf()
print(f"Found {len(result)} rows")
print(result)

print("\nTest VARCHAR cast filter (BROKEN METHOD - current implementation):")
result = conn.execute("""
    SELECT Date, Time 
    FROM worksheet1 
    WHERE CAST(Time AS VARCHAR) >= '2017-01-02 00:00:00'
      AND CAST(Time AS VARCHAR) <= '2017-01-02 23:59:59'
    LIMIT 3
""").fetchdf()
print(f"Found {len(result)} rows")
print(result)

conn.close()

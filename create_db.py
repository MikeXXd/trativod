import sqlite3

conn = sqlite3.connect("trativod.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS measurements (
    timestamp DATETIME NOT NULL,
    distance_mm REAL NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pump_events (
    timestamp DATETIME NOT NULL,
    state TEXT NOT NULL,
    source TEXT NOT NULL
)
""")

cur.execute("""
INSERT OR IGNORE INTO settings(key,value)
VALUES('auto_mode','0')
""")

conn.commit()
conn.close()

print("Database created")

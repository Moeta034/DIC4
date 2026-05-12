import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = 'aiotdb.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            device_id TEXT,
            ip_address TEXT,
            temp REAL,
            humd REAL
        )
    ''')
    
    # Clear existing data if any (optional, but good for a fresh start)
    # c.execute("DELETE FROM sensors")
    
    # Insert mock data
    start_time = datetime.now() - timedelta(minutes=10)
    mock_data = []
    
    for i in range(30):
        timestamp = (start_time + timedelta(seconds=i * 20)).strftime('%Y-%m-%d %H:%M:%S')
        temp = round(random.uniform(22.0, 28.0), 1)
        humd = round(random.uniform(45.0, 65.0), 1)
        mock_data.append(('ESP32_MOCK_INIT', '192.168.1.100', temp, humd, timestamp))
    
    c.executemany('''
        INSERT INTO sensors (device_id, ip_address, temp, humd, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', mock_data)
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized with 30 rows of mock data.")

if __name__ == "__main__":
    init_db()

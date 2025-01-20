import sqlite3

conn = sqlite3.connect('traffic_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS traffic_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    intersection_id INTEGER NOT NULL,
    vehicle_count INTEGER NOT NULL
)
''')

conn.commit()
conn.close()
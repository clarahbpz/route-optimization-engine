import sqlite3
import os
from datetime import datetime
import pandas as pd

# Define the path to the database file (saving it securely in the data/ folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "routing_logs.db")

def init_db():
    """
    Initializes the SQLite database and creates the logs table if it doesn't exist.
    """
    # Connect to SQLite (this creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS route_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            algorithm TEXT,
            origin_node INTEGER,
            destination_node INTEGER,
            distance_meters REAL,
            intersections_count INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized successfully at: {DB_PATH}")

def log_route(algorithm, origin_node, destination_node, distance_meters, intersections_count):
    """
    Inserts a new route calculation record into the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO route_logs (timestamp, algorithm, origin_node, destination_node, distance_meters, intersections_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, algorithm, origin_node, destination_node, distance_meters, intersections_count))
    
    conn.commit()
    conn.close()

def get_all_logs():
    """
    Retrieves all saved route logs as a Pandas DataFrame. 
    Perfect for our future Analytics Dashboard!
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM route_logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

if __name__ == "__main__":
    # Run this script directly to create the database and table
    init_db()
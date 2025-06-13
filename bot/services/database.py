import sqlite3
from datetime import datetime

DB_PATH = "orders.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            origin TEXT,
            destination TEXT,
            vehicle TEXT,
            tonnage INTEGER,
            distance_km REAL,
            duration TEXT,
            per_km REAL,
            fuel_l REAL,
            fuel_price REAL,
            fuel_cost REAL,
            total REAL,
            status TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_order(user_id: int, data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (
            user_id, origin, destination, vehicle, tonnage,
            distance_km, duration, per_km, fuel_l, fuel_price,
            fuel_cost, total, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data["origin"],
        data["destination"],
        data["vehicle"],
        data["tonnage"],
        data["distance_km"],
        data["duration_str"],
        data["per_km"],
        data["fuel_l"],
        data["fuel_price"],
        data["fuel_cost"],
        data["total"],
        "в обробці",
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()

def get_orders_by_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC', (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results
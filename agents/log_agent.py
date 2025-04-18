import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "trade_logs.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_log_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            signal TEXT,
            sentiment TEXT,
            lot REAL,
            price REAL,
            result TEXT,
            pnl REAL
        )
    """)
    conn.commit()
    conn.close()


def log_trade(symbol, signal, sentiment, lot, price, result="pending", pnl=None):
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO logs (timestamp, symbol, signal, sentiment, lot, price, result, pnl)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, symbol, signal, sentiment, lot, price, result, pnl))
    conn.commit()
    conn.close()

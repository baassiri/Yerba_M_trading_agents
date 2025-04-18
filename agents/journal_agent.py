import os
import sqlite3
from datetime import datetime, timedelta
from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "trade_logs.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def fetch_recent_trades(hours=24):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    c.execute("SELECT timestamp, symbol, signal, sentiment, lot, price, result, pnl FROM logs WHERE timestamp > ?", (since,))
    rows = c.fetchall()
    conn.close()
    return rows

def analyze_trades_with_gpt(trades):
    if not trades:
        return "No trades found in the past 24h."

    formatted = "\n".join([f"{r[1]} | {r[2]} | Sentiment: {r[3]} | Lot: {r[4]} | PnL: {r[7]}" for r in trades])
    
    prompt = f"""
Here are the last trades made by my trading bot:

{formatted}

Analyze them and answer:
- Did the bot make good decisions?
- Were there any mistakes or biases?
- Suggest how to improve strategy, timing, or risk management.
- Suggest if any agents need tuning or deactivation.
- Return a short performance journal summary.
"""
    return ask_gpt(prompt, temperature=0.4)

def run_journal_review():
    trades = fetch_recent_trades()
    summary = analyze_trades_with_gpt(trades)
    print("\n📘 Daily Trade Journal:\n")
    print(summary)
    return summary

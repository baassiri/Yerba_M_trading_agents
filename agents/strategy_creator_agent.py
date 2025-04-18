import os
from datetime import datetime
from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump

STRATEGY_DIR = "strategies"
os.makedirs(STRATEGY_DIR, exist_ok=True)

def generate_strategy_code(symbol="XAUUSD_", timeframe="M5"):
    prompt = f"""
You are a Python quant strategy designer. Write a new custom trading strategy for MetaTrader5 backtesting using the `backtesting.py` library.

Requirements:
- Asset: {symbol}
- Timeframe: {timeframe}
- Must subclass `Strategy`
- Use realistic logic (e.g. EMA + RSI or volume spike + candle pattern)
- Include self.init() and self.next()
- No infinite loops, no external data sources
- Return only Python code
"""
    return ask_gpt(prompt, temperature=0.4)

def save_strategy(code: str, filename: str):
    path = os.path.join(STRATEGY_DIR, filename)
    with open(path, "w") as f:
        f.write(code)
    return path

def create_and_store_strategy(symbol="XAUUSD_", name_hint="auto_strategy"):
    print("🧠 Asking GPT to generate strategy...")
    code = generate_strategy_code(symbol)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{name_hint}_{timestamp}.py"
    path = save_strategy(code, filename)
    print(f"✅ Strategy saved to: {path}")
    return path

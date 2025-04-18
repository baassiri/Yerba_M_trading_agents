from XAUUSD_Data.utils.config_loader import load_config
from datetime import datetime
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump

config = load_config()

ema_fast = config["ema_trend_strategy"]["ema_fast"]
ema_slow = config["ema_trend_strategy"]["ema_slow"]
range_window = config["breakout_strategy"]["range_window"]

# === Strategy Definitions ===

def ema_trend_strategy(df):
    df["ema_fast"] = df["close"].ewm(span=ema_fast).mean()
    df["ema_slow"] = df["close"].ewm(span=ema_slow).mean()
    if df["ema_fast"].iloc[-1] > df["ema_slow"].iloc[-1]:
        return "BUY"
    elif df["ema_fast"].iloc[-1] < df["ema_slow"].iloc[-1]:
        return "SELL"
    return "HOLD"

def breakout_strategy(df):
    df["range"] = df["high"] - df["low"]
    recent_range = df["range"].rolling(range_window).mean().iloc[-1]
    if df["close"].iloc[-1] > df["high"].rolling(20).max().iloc[-1] + recent_range:
        return "BUY"
    elif df["close"].iloc[-1] < df["low"].rolling(20).min().iloc[-1] - recent_range:
        return "SELL"
    return "HOLD"

# === Market Session Logic ===

def detect_market_condition(df):
    recent_range = df["high"].max() - df["low"].min()
    avg_candle = df["close"].diff().abs().mean()
    if recent_range > 3 * avg_candle:
        return "volatile"
    elif df["close"].iloc[-1] > df["close"].rolling(20).mean().iloc[-1]:
        return "trending"
    return "ranging"

def get_market_session():
    hour = datetime.utcnow().hour
    if 0 <= hour < 8:
        return "asia"
    elif 7 <= hour < 15:
        return "london"
    elif 12 <= hour < 20:
        return "new_york"
    return "off_hours"

# === Main Decision Logic ===

def generate_signal(df, sentiment=None):
    market_condition = detect_market_condition(df)
    session = get_market_session()

    if session == "asia" and market_condition == "ranging":
        return "HOLD"
    elif session == "london" and market_condition == "trending":
        return ema_trend_strategy(df)
    elif session == "new_york" and market_condition == "volatile":
        return breakout_strategy(df)
    elif sentiment == "very_positive":
        return "BUY"
    elif sentiment == "very_negative":
        return "SELL"
    return "HOLD"

# XAUUSD__Data/utils/context.py

context = {
    "symbol": "XAUUSD_",
    "timeframe": "M5",
    "market_condition": None,
    "session": None,
    "sentiment": None,
    "signal": None,
    "risk_passed": None,
    "lot_size": None,
    "execution_result": None,
    "last_journal": None,
    "improvement_suggestions": None
}

def update(key, value):
    context[key] = value

def get(key):
    return context.get(key)

def dump():
    return context

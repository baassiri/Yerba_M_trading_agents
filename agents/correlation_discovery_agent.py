from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy

def discover_correlated_symbols(master_symbol: str, available_symbols: list, top_n: int = 10):
    prompt = f"""
You are a market correlation analyst AI agent.

The primary asset is: **{master_symbol}**

From the list of available instruments below, analyze and return the top {top_n} symbols that are most likely to be correlated (positively or inversely) with it based on:
- Market structure
- Macro relationships
- Currency or asset class behavior

Available symbols: {available_symbols}

Return a pure JSON list like:
["EURUSD", "USDJPY", "US500"]
"""

    response = ask_gpt(prompt)

    try:
        import json
        return json.loads(response)
    except Exception:
        print("❌ Correlation Discovery Agent: GPT returned malformed output:\n", response)
        return []

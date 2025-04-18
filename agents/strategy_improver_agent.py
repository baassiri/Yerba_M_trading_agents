import os
from datetime import datetime
from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.agents.market_watcher_agent import get_live_data, get_latest_price
from XAUUSD_Data.utils.context import dump

import os
STRATEGY_FOLDER = os.path.join(os.path.dirname(__file__), "..", "strategies")
STRATEGY_FOLDER = os.path.abspath(STRATEGY_FOLDER)
os.makedirs(STRATEGY_FOLDER, exist_ok=True)
def improve_strategy(file_name: str, notes: str = "") -> str:
    file_path = os.path.join(STRATEGY_FOLDER, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Strategy file not found: {file_path}")

    with open(file_path, "r") as f:
        strategy_code = f.read()

    prompt = f"""
You are a professional trading strategist. Improve the following Python strategy code based on these performance notes:

{notes}

Here is the code:
```python
{strategy_code}
"""
    improved_code = ask_gpt(prompt, temperature=0.4)

    base, ext = os.path.splitext(file_name)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    new_file = f"{base}_v2_{timestamp}{ext}"
    new_path = os.path.join(STRATEGY_FOLDER, new_file)

    with open(new_path, "w") as f:
        f.write(improved_code)

    print(f"✅ Improved strategy saved as: {new_path}")
    return new_path

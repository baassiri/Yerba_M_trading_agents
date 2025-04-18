import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "strategy_config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"❌ Config file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(new_config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(new_config, f, indent=2)
    print(f"✅ Config saved to {CONFIG_PATH}")

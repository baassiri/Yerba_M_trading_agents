from XAUUSD_Data.agents.self_improver_agent import run_self_improver
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.agents.conversation_agent import simulate_agent_conversation

from XAUUSD_Data.utils.context import dump
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
import time

def run_orchestrator():
    send_telegram_message("🎬 Starting agent collaboration...")

    # Step 1: Self Improver generates suggestions
    suggestions = run_self_improver(strategy_name="ema", symbol="XAUUSD_")
    send_telegram_message(f"📘 SelfImprov Agent:\n{suggestions}")
    time.sleep(1)

    # Step 2: Strategy Improver acts on those suggestions
    send_telegram_message("🧠 StrategyImprover Agent: Working on improving strategy...")
    improved_path = improve_strategy("ema_strategy.py", suggestions)
    send_telegram_message(f"✅ StrategyImproved and saved as: {improved_path}")
    time.sleep(1)

    # Step 3: Agents discuss final result
    send_telegram_message("🗣️ Running simulated agent roundtable...")
    conversation = simulate_agent_conversation()
    send_telegram_message(f"🤖 Agent Talk:\n{conversation[:4000]}")  # Telegram limit
    time.sleep(1)

    # Final context dump
    summary = dump()
    formatted = "\n".join([f"{k}: {v}" for k, v in summary.items()])
    send_telegram_message(f"📊 Final Agent Context:\n{formatted[:4000]}")
if __name__ == "__main__":
    run_orchestrator()

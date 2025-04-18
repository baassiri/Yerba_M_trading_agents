from XAUUSD_Data.agents.journal_agent import run_journal_review
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.agents.backtesting_agent import run_backtest
from XAUUSD_Data.utils.strategy_selector import get_strategy_by_name
from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import update

def suggest_improvements(journal_summary, backtest_stats):
    prompt = f"""
My trading bot produced the following journal summary and backtest results:

📘 Journal:
{journal_summary}

📊 Backtest Stats:
{backtest_stats}

Please suggest:
- How to improve the strategy logic (e.g., indicators, conditions)
- Changes to risk management (e.g., SL/TP, lot size)
- If certain agents should be disabled or adjusted
- Return the suggestions in bullet form.
"""
    return ask_gpt(prompt, temperature=0.3)

def run_self_improver(strategy_name="ema", symbol="XAUUSD_"):
    print("🧠 Running journal review...")
    journal_summary = run_journal_review()

    print("\n🔁 Running backtest...")
    strategy_class = get_strategy_by_name(strategy_name)
    _, stats = run_backtest(strategy_class, symbol=symbol)

    print("\n🧪 Suggesting improvements via GPT...")
    suggestions = suggest_improvements(journal_summary, str(stats))

    print("\n🚀 Self-Improvement Suggestions:")
    print(suggestions)

    update("improvement_suggestions", suggestions)
    return suggestions

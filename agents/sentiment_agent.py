from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump

def get_sentiment_summary(symbol="XAUUSD_") -> str:
    prompt = f"""
Analyze the market sentiment for {symbol} using recent financial news and social trends.
Is the sentiment positive, neutral, or negative? Summarize it briefly.
Return one of: very_positive, positive, neutral, negative, very_negative.
"""
    try:
        result = ask_gpt(prompt, temperature=0.2).strip().lower()
        return result
    except Exception as e:
        print("❌ Sentiment error:", e)
        return "neutral"

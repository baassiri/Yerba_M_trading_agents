from XAUUSD_Data.utils.context import update, get, dump
from XAUUSD_Data.agents.strategy_agent import generate_signal
from XAUUSD_Data.agents.market_watcher_agent import get_live_data
from XAUUSD_Data.agents.sentiment_agent import get_sentiment_summary
from XAUUSD_Data.agents.risk_manager_agent import can_open_trade, calculate_lot_size
from XAUUSD_Data.agents.trade_executor_agent import place_order
from XAUUSD_Data.agents.log_agent import log_trade
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.config_loader import load_config

def run_trading_round(symbol="XAUUSD_"):
    print("🎯 Market Watcher: Fetching data...")
    df = get_live_data(symbol)
    update("latest_data", df)

    print("🧠 Sentiment Agent: Reading market tone...")
    sentiment = get_sentiment_summary(symbol)
    update("sentiment", sentiment)

    print("📈 Strategy Agent: Generating signal...")
    signal = generate_signal(df, sentiment=sentiment)
    update("signal", signal)
    print(f"🧠 Signal decided: {signal}")

    print("🛡 Risk Agent: Verifying trade constraints...")
    allowed, reason = can_open_trade()
    update("risk_passed", allowed)

    if not allowed:
        print(f"🛑 Risk blocked trade: {reason}")
        return {"status": "blocked", "reason": reason}

    lot = calculate_lot_size(symbol, stop_loss_pips=100)
    update("lot_size", lot)
    print(f"✅ Lot size approved: {lot}")

    print("🤖 Executor Agent: Executing order...")
    execution_result = place_order(symbol, signal, lot)
    update("execution_result", execution_result)

    print("📝 Logger Agent: Logging trade...")
    log_trade(symbol, signal, sentiment, lot, df['close'].iloc[-1], result=execution_result)

    # Final log
    final_summary = "\n".join([f"{k}: {v}" for k, v in dump().items()])
    print("\n🧾 Final Round Summary:\n" + final_summary)

    return {"status": "executed", "summary": final_summary}

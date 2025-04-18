import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump

def initialize_mt5():
    if not mt5.initialize():
        raise Exception("❌ Failed to initialize MT5")
    print("✅ MT5 initialized")

def shutdown_mt5():
    mt5.shutdown()
    print("🔌 MT5 shutdown")

def get_live_data(symbol="XAUUSD_", timeframe=mt5.TIMEFRAME_M5, bars=100):
    if not mt5.initialize():
        raise Exception("❌ MT5 failed to initialize for live data.")
    
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    mt5.shutdown()

    if rates is None:
        raise Exception(f"❌ Failed to get data for {symbol}")
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def get_latest_price(symbol="XAUUSD_"):
    if not mt5.initialize():
        raise Exception("❌ MT5 failed to initialize for price.")
    
    tick = mt5.symbol_info_tick(symbol)
    mt5.shutdown()

    if tick is None:
        raise Exception(f"❌ Failed to get tick for {symbol}")
    return tick.ask, tick.bid

# Test mode
if __name__ == "__main__":
    from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy

    try:
        df = get_live_data()
        print(df.tail())

        ask, bid = get_latest_price()
        print(f"Ask: {ask}, Bid: {bid}")
    except Exception as e:
        print(e)
        send_telegram_message(f"Error: {e}")
        dump(e, "error_log.txt")
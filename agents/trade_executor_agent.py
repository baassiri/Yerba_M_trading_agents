import MetaTrader5 as mt5
from XAUUSD_Data.utils.config_loader import load_config
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import update
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy

config = load_config()

SL_PIPS = config["execution"]["sl_pips"]
TP_PIPS = config["execution"]["tp_pips"]
DEVIATION = config["execution"]["deviation"]

def place_order(symbol, signal, lot):
    if not mt5.initialize():
        raise Exception("❌ Failed to initialize MT5 for order placement")

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        mt5.shutdown()
        raise Exception(f"❌ Failed to get tick for {symbol}")

    price = tick.ask if signal == "BUY" else tick.bid
    sl = price - SL_PIPS * 0.1 if signal == "BUY" else price + SL_PIPS * 0.1
    tp = price + TP_PIPS * 0.1 if signal == "BUY" else price - TP_PIPS * 0.1
    order_type = mt5.ORDER_TYPE_BUY if signal == "BUY" else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": 123456,
        "comment": "Ultimate AI Trader",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    mt5.shutdown()

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Trade failed: {result.retcode}")
        return f"❌ Error: {result.retcode}"

    print(f"✅ Trade placed: {signal} {symbol} @ {price}")
    return "✅ Trade executed"

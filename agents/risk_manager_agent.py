import MetaTrader5 as mt5
from XAUUSD_Data.utils.config_loader import load_config
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import update

config = load_config()

MAX_RISK_PERCENT = config["risk_management"]["max_risk_percent"]
MAX_OPEN_TRADES = config["risk_management"]["max_open_trades"]
ACCOUNT_BALANCE_MIN = config["risk_management"]["account_balance_min"]

def get_account_info():
    if not mt5.initialize():
        raise Exception("❌ Failed to initialize MT5 for account info")

    account = mt5.account_info()
    mt5.shutdown()

    if account is None:
        raise Exception("❌ Failed to get account info")

    return account.balance, account.equity

def can_open_trade():
    balance, _ = get_account_info()

    if not mt5.initialize():
        raise Exception("❌ Failed to initialize MT5 for positions")
    
    positions = mt5.positions_get()
    mt5.shutdown()

    open_trades = len(positions) if positions else 0

    if balance < ACCOUNT_BALANCE_MIN:
        return False, "💸 Not enough balance"
    if open_trades >= MAX_OPEN_TRADES:
        return False, "🔒 Max open trades reached"

    return True, "✅ Trade allowed"

def calculate_lot_size(symbol, stop_loss_pips=100):
    balance, _ = get_account_info()
    risk_usd = (MAX_RISK_PERCENT / 100) * balance

    if not mt5.initialize():
        raise Exception("❌ Failed to initialize MT5 for symbol info")
    
    symbol_info = mt5.symbol_info(symbol)
    mt5.shutdown()

    if not symbol_info:
        raise Exception(f"❌ Failed to get symbol info for {symbol}")
    
    tick_value = symbol_info.trade_tick_value
    lot_size = risk_usd / (stop_loss_pips * tick_value)

    return round(min(lot_size, symbol_info.volume_max), 2)

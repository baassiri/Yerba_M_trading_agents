import MetaTrader5 as mt5
import pandas as pd

from XAUUSD_Data.agents.correlation_discovery_agent import discover_correlated_symbols
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy

def fetch_price_data(symbol, timeframe=mt5.TIMEFRAME_M5, bars=200):
    if not mt5.initialize():
        raise Exception("❌ MT5 init failed")
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    mt5.shutdown()

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    df.rename(columns={"close": symbol}, inplace=True)
    return df[[symbol]]

def compute_correlation_matrix(symbols, bars=200):
    all_data = []
    for symbol in symbols:
        try:
            df = fetch_price_data(symbol, bars=bars)
            all_data.append(df)
        except Exception as e:
            print(f"⚠️ Skipped {symbol}: {e}")
    if not all_data:
        return None
    merged = pd.concat(all_data, axis=1).dropna()
    return merged.corr()

def find_correlations_for(symbol="XAUUSD_", available_symbols=None, threshold=0.7):
    if available_symbols is None:
        available_symbols = ["XAUUSD__", "EURUSD_", "USDJPY_", "GBPUSD_", "USDCHF_"]

    selected = discover_correlated_symbols(symbol, available_symbols)
    selected = list(set(selected + [symbol]))  # Ensure symbol is included
    corr_matrix = compute_correlation_matrix(selected)

    if corr_matrix is None or symbol not in corr_matrix:
        return []

    results = []
    for other in corr_matrix.columns:
        if other != symbol:
            corr = corr_matrix.loc[symbol, other]
            if abs(corr) >= threshold:
                results.append((other, round(corr, 3)))
    return sorted(results, key=lambda x: abs(x[1]), reverse=True)

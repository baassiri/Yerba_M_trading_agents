import MetaTrader5 as mt5
import pandas as pd
import joblib
from backtesting import Backtest, Strategy
from XAUUSD_Data.utils.strategy_selector import get_strategy_by_name
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.utils.context import dump
from datetime import datetime

# === Load Historical MT5 Data ===
def get_historical_data(symbol="XAUUSD_", timeframe=mt5.TIMEFRAME_M5, bars=1000):
    if not mt5.initialize():
        raise Exception("❌ Failed to initialize MT5")
        
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    mt5.shutdown()

    if rates is None:
        raise Exception(f"❌ Failed to retrieve data for {symbol}")
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)
    df = df[['time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return df.set_index('time')

import pandas as pd

class EmaCrossStrategy(Strategy):
    def init(self):
        close_series = pd.Series(self.data.Close)
        self.ema50 = self.I(lambda: close_series.ewm(span=50).mean())
        self.ema200 = self.I(lambda: close_series.ewm(span=200).mean())

    def next(self):
        if self.ema50[-1] > self.ema200[-1] and self.ema50[-2] <= self.ema200[-2]:
            self.buy()
        elif self.ema50[-1] < self.ema200[-1] and self.ema50[-2] >= self.ema200[-2]:
            self.sell()


# === ML Strategy ===
class MLStrategy(Strategy):
    def init(self):
        self.model = joblib.load("models/my_model.pkl")
        self.lookback = 10
        self.df = self.data.df

    def next(self):
        if len(self.df) < self.lookback:
            return
        X = self.df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(self.lookback).values.flatten().reshape(1, -1)
        pred = self.model.predict(X)[0]

        if pred == 1 and not self.position:
            self.buy()
        elif pred == -1 and not self.position:
            self.sell()

# === Run Backtest ===
def run_backtest(strategy_class, symbol="XAUUSD_", timeframe=mt5.TIMEFRAME_M5, bars=1000):
    df = get_historical_data(symbol, timeframe, bars)
    bt = Backtest(df, strategy_class, cash=10_000, commission=0.0005)
    stats = bt.run()
    return bt, stats

# === CLI Start ===
if __name__ == "__main__":
    strategy_name = "ml"  # "ema" or "ml"
    strategy_class = get_strategy_by_name(strategy_name)

    bt, stats = run_backtest(strategy_class, symbol="XAUUSD_")
    print(stats)
    bt.plot()

from backtesting import Strategy
import pandas as pd

class EmaCrossStrategy(Strategy):
    def init(self):
        self.ema50 = self.I(lambda x: pd.Series(x).ewm(span=50).mean(), self.data.Close)
        self.ema200 = self.I(lambda x: pd.Series(x).ewm(span=200).mean(), self.data.Close)

    def next(self):
        if self.ema50[-1] > self.ema200[-1] and self.ema50[-2] <= self.ema200[-2]:
            self.buy()
        elif self.ema50[-1] < self.ema200[-1] and self.ema50[-2] >= self.ema200[-2]:
            self.sell()

Here's the improved code:

```python
from backtesting import Strategy
import pandas as pd
from talib import RSI, MACD, BBANDS

class EmaCrossStrategy(Strategy):
    def init(self):
        self.ema50 = self.I(lambda x: pd.Series(x).ewm(span=50).mean(), self.data.Close)
        self.ema200 = self.I(lambda x: pd.Series(x).ewm(span=200).mean(), self.data.Close)
        self.rsi = self.I(lambda x: RSI(x, timeperiod=14), self.data.Close)
        self.macd = self.I(lambda x: MACD(x, fastperiod=12, slowperiod=26, signalperiod=9)[0], self.data.Close)
        self.upper, self.middle, self.lower = self.I(lambda x: BBANDS(x, timeperiod=20), self.data.Close)

    def next(self):
        if self.ema50[-1] > self.ema200[-1] and self.ema50[-2] <= self.ema200[-2] and self.rsi[-1] < 30 and self.macd[-1] > 0:
            self.buy()
        elif self.ema50[-1] < self.ema200[-1] and self.ema50[-2] >= self.ema200[-2] and self.rsi[-1] > 70 and self.macd[-1] < 0:
            self.sell()

        # Adding stop loss and take profit levels
        if self.position.is_long and self.data.Close[-1] < self.lower[-1]:
            self.position.close()
        elif self.position.is_short and self.data.Close[-1] > self.upper[-1]:
            self.position.close()
```

In this code, we have incorporated RSI, MACD, and Bollinger Bands into our strategy. We have also added conditions to our buy and sell signals based on these indicators. For instance, we only buy when the RSI is below 30 (indicating the asset is oversold) and the MACD line is above the signal line (indicating bullish momentum). Similarly, we only sell when the RSI is above 70 (indicating the asset is overbought) and the MACD line is below the signal line (indicating bearish momentum).

We have also added stop loss and take profit levels based on the Bollinger Bands. If we are in a long position and the price falls below the lower band, we close the position. Similarly, if we are in a short position and the price rises above the upper band, we close the position. This helps us manage our risk and protect our capital.
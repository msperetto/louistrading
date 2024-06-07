from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas_ta as ta
import pandas as pd

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()


class PlaygroundLouis(Strategy):
    sma_period1 = 0
    sma_period2 = 0
    rsi_period = 0
    rsi_layer1 = 0
    rsi_layer2 = 0

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.sma_period1)
        self.sma2 = self.I(SMA, self.data.Close, self.sma_period2)
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_period)

    def next(self):
        if self.rsi < self.rsi_layer1:

        # if (crossover(self.sma1, self.sma2) and self.rsi < self.rsi_layer1):
            # self.position.close()
            self.buy()

        elif self.rsi > self.rsi_layer2:
            self.position.close()
            # self.sell()
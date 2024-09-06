from filter import Filter, FilterBuy_RSI, FilterBuy_RSI_SMA, FilterSell_RSI
from trigger import TriggeredState, TriggeredState_MaxCandles, TriggeredState_MaxCandles_LongSma
from trade import Trade, Trade_Buy_HighLastCandle, Trade_Sell_LowLastCandle
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas_ta as ta
import pandas as pd
from time import sleep


class PlaygroundLouis(Strategy):
    sma_period_medium = 0
    sma_period_long = 0
    rsi_period = 0
    rsi_layer_cheap = 0
    rsi_layer_expensive = 0
    triggered = False
    candles_after_triggered = 0
    max_candles = 0
    # filter = None
    # triggeredState = None
    # trade = None

    def init(self):
        #initializing technical indicators
        self.sma1 = self.I(ta.sma, pd.Series(self.data.Close), self.sma_period_medium)
        self.sma2 = self.I(ta.sma, pd.Series(self.data.Close), self.sma_period_long)
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_period)

        #instantiating buying support objects
        self.filterBuy = FilterBuy_RSI(lambda: self.rsi[:len(self.rsi)], self.rsi_layer_cheap)
        self.triggeredStateBuy = TriggeredState_MaxCandles(self.max_candles)
        self.tradeBuy = Trade_Buy_HighLastCandle(self.data)

        #instantiating selling support objects
        self.filterSell = FilterSell_RSI(lambda: self.rsi[:len(self.rsi)], self.rsi_layer_expensive)
        self.triggeredStateSell = TriggeredState_MaxCandles(self.max_candles)
        self.tradeSell = Trade_Sell_LowLastCandle(self.data)

        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggeredStateBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggeredStateSell, self.tradeSell)

    def next(self):
        if self.strategyBuy.shouldBuy(): self.buy()
        if self.strategySell.shouldSell(): self.position.close()

    
class StrategyBuy():
    def __init__(self, filterBuy, triggeredState, trade):
        self.filter = filterBuy
        self.triggeredState = triggeredState
        self.trade = trade

    def shouldBuy(self):
        if self.filter.isValid(): 
            self.triggeredState.reset()

        if self.triggeredState.isStillValid():
            if self.trade.buyConfirmation(): return True
        

class StrategySell():
    def __init__(self, filterSell, triggeredState, trade):
        self.filter = filterSell
        self.triggeredState = triggeredState
        self.trade = trade

    def shouldSell(self):
        if self.filter.isValid():
            self.triggeredState.reset()

        if self.triggeredState.isStillValid():
            if self.trade.sellConfirmation(): return True
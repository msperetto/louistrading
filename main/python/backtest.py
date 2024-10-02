from filter import Filter, FilterBuy_RSI, FilterSell_RSI, FilterBuy_RSI_price_SMAlong
from trigger import TriggeredState, TriggeredState_MaxCandles, TriggeredState_MaxCandles_LongSma
from trade import Trade, TradeBuy_HighLastCandle, TradeSell_LowLastCandle, TradeBuy_High_x_HighLastCandle, TradeSell_Price_EMAshort
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas_ta as ta
import pandas as pd
from time import sleep


class PlaygroundLouis(Strategy):
    sma_p_short = 0
    sma_p_medium = 0
    sma_p_long = 0
    ema_p_short = 0
    ema_p_medium = 0
    ema_p_long = 0
    rsi_period = 0
    rsi_layer_cheap = 0
    rsi_layer_expensive = 0
    triggered = False
    candles_after_triggered = 0
    max_candles_buy = 0
    max_candles_sell = 0
    filter_buy_class = "self.filterBuy = FilterBuy_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap)"
    trigger_buy_class = "self.triggerBuy = TriggeredState_MaxCandles(self.max_candles_buy)"
    trade_buy_class = "self.tradeBuy = Trade_Buy_HighLastCandle(self.data)"
    filter_sell_class = "self.filterSell = FilterSell_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_expensive)"
    trigger_sell_class = "self.triggerSell = TriggeredState_MaxCandles(self.max_candles_sell)"
    trade_sell_class = "self.tradeSell = Trade_Sell_LowLastCandle(self.data)"


    def init(self):
        self.classes = {}
        #initializing technical indicators
        self.ema_short = self.I(ta.ema, pd.Series(self.data.Close), self.ema_p_short)
        self.ema_medium = self.I(ta.ema, pd.Series(self.data.Close), self.ema_p_medium)
        self.ema_long = self.I(ta.ema, pd.Series(self.data.Close), self.ema_p_long)

        self.sma_short = self.I(ta.sma, pd.Series(self.data.Close), self.sma_p_short)
        self.sma_medium = self.I(ta.sma, pd.Series(self.data.Close), self.sma_p_medium)
        self.sma_long = self.I(ta.sma, pd.Series(self.data.Close), self.sma_p_long)
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_period)

        #instantiating buying support objects
        exec(self.filter_buy_class)
        exec(self.trigger_buy_class)
        exec(self.trade_buy_class)

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.filterBuy.__class__.__name__
        self.classes['trigger_buy'] = self.triggerBuy.__class__.__name__
        self.classes['trade_buy']= self.tradeBuy.__class__.__name__

        #instantiating selling support objects
        exec(self.filter_sell_class)
        exec(self.trigger_sell_class)
        exec(self.trade_sell_class)
        
        #adding classes name to stats list to populate DB
        self.classes['filter_sell'] = self.filterSell.__class__.__name__
        self.classes['trigger_sell'] = self.triggerSell.__class__.__name__
        self.classes['trade_sell'] = self.tradeSell.__class__.__name__


        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)

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
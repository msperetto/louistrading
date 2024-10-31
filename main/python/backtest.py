from filter import *
from trigger import *
from trade import *
from trend import *
from backtesting import Backtest, Strategy
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd
from time import sleep
from strategy import *

class NoShirt(Strategy):
    ema_trend_short = 0
    sma_trend_medium = 0
    sma_trend_long = 0
    adr_trend_layer = 0
    trend_interval = "D"
    sma_p_short = 0
    sma_p_medium = 0
    sma_p_long = 0
    ema_p_short = 0
    ema_p_medium = 0
    ema_p_long = 0
    rsi_period = 0
    rsi_layer_cheap = 0
    rsi_layer_expensive = 0
    # triggered = False
    candles_after_triggered = 0
    max_candles_buy = 0
    max_candles_sell = 0
    stop_loss = None
    take_profit = None
    trend_class = "self.trend = AlwaysTrend()"
    filter_buy_class = "self.filterBuy = FilterBuy_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap)"
    trigger_buy_class = "self.triggerBuy = TriggeredState_MaxCandles(self.max_candles_buy)"
    trade_buy_class = "self.tradeBuy = TradeBuy_HighLastCandle(self.data)"
    filter_sell_class = "self.filterSell = FilterSell_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_expensive)"
    trigger_sell_class = "self.triggerSell = TriggeredState_MaxCandles(self.max_candles_sell)"
    trade_sell_class = "self.tradeSell = TradeSell_LowLastCandle(self.data)"


    def init(self):
        self.classes = {}

        if self.ema_p_short != 0: self.ema_short = self.I(ta.ema, pd.Series(self.data.Close), self.ema_p_short)
        if self.ema_p_medium != 0: self.ema_medium = self.I(ta.ema, pd.Series(self.data.Close), self.ema_p_medium)
        if self.ema_p_long != 0: self.ema_long = self.I(ta.ema, pd.Series(self.data.Close), self.ema_p_long)

        if self.sma_p_short != 0: self.sma_short = self.I(ta.sma, pd.Series(self.data.Close), self.sma_p_short)
        if self.sma_p_medium != 0: self.sma_medium = self.I(ta.sma, pd.Series(self.data.Close), self.sma_p_medium)
        if self.sma_p_long != 0: self.sma_long = self.I(ta.sma, pd.Series(self.data.Close), self.sma_p_long)
        if self.rsi_period != 0: self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_period)

        if self.ema_trend_short != 0: self.ema_trend_short = resample_apply(self.trend_interval, ta.ema, self.data.Close, self.ema_trend_short)
        if self.sma_trend_medium != 0: self.sma_trend_medium = resample_apply(self.trend_interval, ta.sma, self.data.Close, self.sma_trend_medium)
        if self.sma_trend_long != 0: self.sma_trend_long = resample_apply(self.trend_interval, ta.sma, self.data.Close, self.sma_trend_long)

        #instantiating buying support objects
        exec(self.filter_buy_class)
        exec(self.trigger_buy_class)
        exec(self.trade_buy_class)
        exec(self.trend_class)

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.filterBuy.__class__.__name__
        self.classes['trigger_buy'] = self.triggerBuy.__class__.__name__
        self.classes['trade_buy']= self.tradeBuy.__class__.__name__
        self.classes['trend'] = self.trend.__class__.__name__

        #instantiating selling support objects
        exec(self.filter_sell_class)
        exec(self.trigger_sell_class)
        exec(self.trade_sell_class)
        
        #adding classes name to stats list to populate DB
        self.classes['filter_sell'] = self.filterSell.__class__.__name__
        self.classes['trigger_sell'] = self.triggerSell.__class__.__name__
        self.classes['trade_sell'] = self.tradeSell.__class__.__name__


        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy, self.trend)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)

    def next(self):
        if self.stop_loss:
            stop_loss = self.data.Close[-1] * ((100-self.stop_loss)/100)
        else: stop_loss = None
        if self.take_profit:
            take_profit = self.data.Close[-1] * ((100+self.take_profit)/100)
        else: take_profit = None

        if self.strategyBuy.shouldBuy(): self.buy(sl=stop_loss, tp=take_profit)
        if self.strategySell.shouldSell(): self.position.close()



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
    stop_loss = None
    take_profit = None
    filter_buy_class = "self.filterBuy = FilterBuy_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap)"
    trigger_buy_class = "self.triggerBuy = TriggeredState_MaxCandles(self.max_candles_buy)"
    trade_buy_class = "self.tradeBuy = TradeBuy_HighLastCandle(self.data)"
    filter_sell_class = "self.filterSell = FilterSell_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_expensive)"
    trigger_sell_class = "self.triggerSell = TriggeredState_MaxCandles(self.max_candles_sell)"
    trade_sell_class = "self.tradeSell = TradeSell_LowLastCandle(self.data)"


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
        if self.stop_loss:
            stop_loss = self.data.Close[-1] * ((100-self.stop_loss)/100)
        else: stop_loss = None
        if self.take_profit:
            take_profit = self.data.Close[-1] * ((100+self.take_profit)/100)
        else: take_profit = None

        if self.strategyBuy.shouldBuy(): self.buy(sl=stop_loss, tp=take_profit)
        if self.strategySell.shouldSell(): self.position.close()

    
class StrategyBuy():
    def __init__(self, filterBuy, triggeredState, trade, trend):
        self.filter = filterBuy
        self.triggeredState = triggeredState
        self.trade = trade
        self.trend = trend

    def shouldBuy(self):
        if self.filter.isValid(): 
            self.triggeredState.reset(True)
        else: self.triggeredState.reset(False)

        if self.triggeredState.isStillValid():
            if self.trend.ontrend():
                if self.trade.buyConfirmation(): return True
        

class StrategySell():
    def __init__(self, filterSell, triggeredState, trade):
        self.filter = filterSell
        self.triggeredState = triggeredState
        self.trade = trade

    def shouldSell(self):
        if self.filter.isValid():
            self.triggeredState.reset(True)
        else: self.triggeredState.reset(False)

        if self.triggeredState.isStillValid():
            if self.trade.sellConfirmation(): return True
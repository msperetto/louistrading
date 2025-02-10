from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from backtesting import Strategy
from backtesting.lib import resample_apply
from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.strategy import *

class BacktestManager(Strategy):
    trend_ema_short = 0
    trend_sma_medium = 0
    trend_sma_long = 0
    intraday_adx = 0
    adx_trend_layer = 0
    intraday_interval = "h"
    trend_interval = "D"
    intraday_sma_short = 0
    intraday_sma_medium = 0
    intraday_sma_long = 0
    intraday_ema_short = 0
    intraday_ema_medium = 0
    intraday_ema_long = 0
    intraday_rsi = 0
    intraday_rsi_layer_cheap = 0
    intraday_rsi_layer_expensive = 0
    candles_after_triggered = 0
    intraday_max_candles_buy = 0
    intraday_max_candles_sell = 0
    stop_loss = None
    take_profit = None
    trend_longest_indicator_value = 40
    trend_class = "self.trend = UpTrend_AlwaysTrend()"
    filter_buy_class = "self.filterBuy = Filter_alwaysTrue()"
    trigger_buy_class = "self.triggerBuy = TriggeredState_alwaysTrue()"
    trade_buy_class = "self.tradeBuy = TradeBuy_HighLastCandle(self.data)"
    filter_sell_class = "self.filterSell = Filter_alwaysTrue()"
    trigger_sell_class = "self.triggerSell = TriggeredState_alwaysTrue()"
    trade_sell_class = "self.tradeSell = TradeSell_LowLastCandle(self.data)"

    def init(self):
        # TODO: Maybe change the concept of "strategy" to use the new class design, which uses a parent StrategyLong class.
        # Doing that, I believe all of the code of this class can be simplified.

        self.classes = {}

        if self.intraday_ema_short != 0: self.intraday_ema_short = self.I(ta.ema, pd.Series(self.data.Close), self.intraday_ema_short)
        if self.intraday_ema_medium != 0: self.intraday_ema_medium = self.I(ta.ema, pd.Series(self.data.Close), self.intraday_ema_medium)
        if self.intraday_ema_long != 0: self.intraday_ema_long = self.I(ta.ema, pd.Series(self.data.Close), self.intraday_ema_long)
        if self.intraday_adx != 0: self.intraday_adx = self.I(ta.adx, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close), self.intraday_adx)

        if self.intraday_sma_short != 0: self.intraday_sma_short = self.I(ta.sma, pd.Series(self.data.Close), self.intraday_sma_short)
        if self.intraday_sma_medium != 0: self.intraday_sma_medium = self.I(ta.sma, pd.Series(self.data.Close), self.intraday_sma_medium)
        if self.intraday_sma_long != 0: self.intraday_sma_long = self.I(ta.sma, pd.Series(self.data.Close), self.intraday_sma_long)
        if self.intraday_rsi != 0: self.intraday_rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.intraday_rsi)

        if self.trend_ema_short != 0: self.trend_ema_short = resample_apply(self.trend_interval, ta.ema, self.data.Close, self.trend_ema_short)
        if self.trend_sma_medium != 0: self.trend_sma_medium = resample_apply(self.trend_interval, ta.sma, self.data.Close, self.trend_sma_medium)
        if self.trend_sma_long != 0: self.trend_sma_long = resample_apply(self.trend_interval, ta.sma, self.data.Close, self.trend_sma_long)

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
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)
        self.trendAnalysis = TrendAnalysis(self.trend)

    def next(self):
        # TODO: We might need a new parameter to this class saying if it's LONG or SHORT position.
        
        stop_loss = self.calculate_stop_loss()
        take_profit = self.calculate_take_profit()

        # TODO: Ideally, this "trendAnalysis.is_upTrend" should actually be inside of the strategy class.
        # Notice that we want to be able to run this class even when trying to "discovery an intrady strategy". 
        # So, the concept of trend would not defined yet.
        if self.trendAnalysis.is_upTrend():
            if self.strategyBuy.shouldBuy(): self.buy(sl=stop_loss, tp=take_profit)
        else:
            #keeps updating trigger status even if not on trend
            self.strategyBuy.triggeredState.isStillValid()

        if self.strategySell.shouldSell(): self.position.close()

    def calculate_stop_loss(self):
        """
        Calculates the stop loss based on the most recent closing price and the configured percentage.
        """
        if self.stop_loss:
            return self.data.Close[-1] * ((100 - self.stop_loss) / 100)
        return None

    def calculate_take_profit(self):
        """
        Calculates the take profit based on the most recent closing price and the configured percentage.
        """
        if self.take_profit:
            return self.data.Close[-1] * ((100 + self.take_profit) / 100)
        return None
from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from backtesting import Strategy
from backtesting.lib import resample_apply
from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis
from common.enums import Side_Type
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.strategy import *

class BacktestManagerIntraday(Strategy):
    operation_type = None
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
    trend_class = "UpTrend_AlwaysTrend"
    filter_buy_class = "Filter_alwaysTrue"
    trigger_buy_class = "TriggeredState_alwaysTrue"
    trade_buy_class = "TradeBuy_HighLastCandle"
    filter_sell_class = "Filter_alwaysTrue"
    trigger_sell_class = "TriggeredState_alwaysTrue"
    trade_sell_class = "TradeSell_LowLastCandle"

    def init(self):
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

        #getting all class attributes to pass to buying and selling support objects
        self.attributes = {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not isinstance(getattr(self, attr), type(self.init))}

        #instantiating buying support objects
        self.filterBuy = Filter().filter_factory(self.filter_buy_class, self, **self.attributes)
        self.triggerBuy = TriggeredState().trigger_factory(self.trigger_buy_class, self, **self.attributes)
        self.tradeBuy = Trade().trade_factory(self.trade_buy_class, self, **self.attributes)
        self.trend = Trend().trend_factory(self.trend_class, self, **self.attributes)

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.filterBuy.__class__.__name__
        self.classes['trigger_buy'] = self.triggerBuy.__class__.__name__
        self.classes['trade_buy']= self.tradeBuy.__class__.__name__
        self.classes['trend'] = self.trend.__class__.__name__

        #instantiating selling support objects
        self.filterSell = Filter().filter_factory(self.filter_sell_class, self, **self.attributes)
        self.triggerSell = TriggeredState().trigger_factory(self.trigger_sell_class, self, **self.attributes)
        self.tradeSell = Trade().trade_factory(self.trade_sell_class, self, **self.attributes)

        #adding classes name to stats list to populate DB
        self.classes['filter_sell'] = self.filterSell.__class__.__name__
        self.classes['trigger_sell'] = self.triggerSell.__class__.__name__
        self.classes['trade_sell'] = self.tradeSell.__class__.__name__

        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)
        self.trendAnalysis = TrendAnalysis(self.trend)

    def next(self):
        if (self.operation_type == Side_Type.LONG):
            self.handle_long_position()
        elif (self.operation_type == Side_Type.SHORT):
            self.handle_short_position()

    def handle_long_position(self):
        stop_loss = self.calculate_stop_loss()
        take_profit = self.calculate_take_profit()

        self.try_open_long_position(stop_loss, take_profit)
        self.try_close_long_position()

    def try_open_long_position(self, stop_loss, take_profit):
        # In case there's a opened position, just skip the logic. 
        if self.position: return

        # TODO: Drop self.trendAnalysis.is_upTrend() from this classe. 
        # That shold be used on BacktestManagerStrategy and ideally inside of the strategy class.

        # Ideally, this "trendAnalysis.is_upTrend" should actually be inside of the strategy class.
        # Notice that we want to be able to run this class even when trying to "discovery an intrady strategy". 
        # So, the concept of trend would not defined yet.
        if self.trendAnalysis.is_upTrend():
            if self.strategyBuy.shouldBuy(): self.buy(sl=stop_loss, tp=take_profit)
        else:
            #keeps updating trigger status even if not on trend
            self.strategyBuy.triggeredState.isStillValid()

    def try_close_long_position(self):
        if self.strategySell.shouldSell(): self.position.close()
        
    def handle_short_position(self):
        self.try_open_short_position()
        self.try_close_short_position()

    def try_open_short_position(self):
        # In case there's a opened position, just skip the logic. 
        if self.position: return

        if self.strategySell.shouldSell(): self.sell()

    def try_close_short_position(self):
        if self.strategyBuy.shouldBuy(): self.position.close()

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
import importlib
import pkgutil

from config.config import STRATEGIES_PATH, STRATEGIES_MODULE
from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from backtesting import Backtest, Strategy
from backtesting.lib import resample_apply
from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.strategy import *

# Dynamically import all modules from the common/strategies folder
def import_all_strategies():
    for module_info in pkgutil.iter_modules([str(STRATEGIES_PATH)]):
        print("Importing all strategies")
        module = importlib.import_module(f"{STRATEGIES_MODULE}.{module_info.name}")
        globals().update({name: cls for name, cls in module.__dict__.items() if isinstance(cls, type)})
        print(globals())

# It deals with a single strategy (passed as a parameter) 
class BacktestManagerStrategy(Strategy):
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
    strategy_class = None

    def init(self):
        # import_all_strategies()

        # print(f"Strategy B1A: {Strategy_B1A}")
        # print(f"strategy B2B: {Strategy_B2B}")

        print(f"Strategy class is: {globals().get(self.strategy_class)}")
        # self.position = None # Not sure if we really need this. Perhaps position is already initialized by Backtesting.Strategy
        # Maybe set somehow all necessary classes used by the strategies parameter

        self.strategy = globals().get(self.strategy_class)()

    def next(self):
        # maybe deal with stop loss and stop gain?
        self.try_open_position()
        self.try_close_position()
         
    # try open position
    def try_open_position(self):
        if isinstance(self.strategy, StrategyLong):
            if self.strategy.shouldOpen():
                self.buy()
                return
        # elif isinstance(self.strategy, StrategyShort):
        #     if self.strategy.shouldOpen():
        #         self.sell()
        #         return

    # try close position
    def try_close_position(self):
        if not self.position:
            # In case there's no opened position, just skip the logic. 
            return

        if self.strategy .shouldClose():
            if isinstance(self.strategy , StrategyLong):
                # We could potentially track which strategy close the position.
                # print(f"Closing a LONG position with {strategy.__class__.__name__}")
                self.sell()
            # elif isinstance(self.strategy , StrategyShort):
            #     # We could potentially track which strategy close the position.
            #     # print(f"Closing a SHORT position with {strategy.__class__.__name__}")
            #     self.buy()
            return
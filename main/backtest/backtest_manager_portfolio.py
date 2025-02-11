from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from backtesting import Backtest, Strategy
from backtesting.lib import resample_apply
from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis
from common.strategyLong import StrategyLong
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.strategy import *

# It deals with a single strategy (passed as a parameter) 
class BacktestManagerStrategy(Strategy):
    strategyName = ''

    # def init(self):
        # TODO: Define strategy class
        # self.strategy 

    def next(self):
        # maybe deal with stop loss and stop gain?
        self.try_open_position()
        self.try_close_position()
         
    # try open position
    def try_open_position(self):
        for strategy in self.strategies:
            if isinstance(strategy, StrategyLong):
                if strategy.shouldOpen():
                    self.buy()
                    return
            elif isinstance(strategy, StrategyShort):
                if strategy.shouldOpen():
                    self.sell()
                    return

    # try close position
    def try_close_position(self):
        if not self.position:
            # In case there's no opened position, just skip the logic. 
            return

        for strategy in self.strategies:
            if strategy.shouldClose():
                if isinstance(strategy, StrategyLong):
                    # We could potentially track which strategy close the position.
                    # print(f"Closing a LONG position with {strategy.__class__.__name__}")
                    self.sell()
                elif isinstance(strategy, StrategyShort):
                    # We could potentially track which strategy close the position.
                    # print(f"Closing a SHORT position with {strategy.__class__.__name__}")
                    self.buy()
                return

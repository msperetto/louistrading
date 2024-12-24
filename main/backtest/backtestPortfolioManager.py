from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from backtesting import Backtest, Strategy
from backtesting.lib import resample_apply
from main.common.strategybuy import StrategyBuy
from main.common.strategysell import StrategySell
from main.common.trendanalysis import TrendAnalysis
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.strategy import *

# It deals with a list of strategies. 
class BacktestPortfolioManager(Strategy):
    def __init__(self, strategies):
        self.strategies = strategies  
        self.position = None # Not sure if we really need this. Perhaps position is already initialized by Backtesting.Strategy
        # Maybe set somehow all necessary classes used by the strategies parameter


    def next(self):
        # maybe deal with stop loss and stop gain?

        self.try_open_position()
        self.try_close_position()
         

    # try open position
    def try_open_position(self):
        for strategy in self.strategies:
            if strategy.ShouldBuy():
                self.buy()
                return

    # try close position
    def try_close_position(self):
        if not self.position:
            # In case there's no opened position, just skip the logic. 
            return

        for strategy in self.strategies:
            if strategy.ShouldSell():
                # We could potentially track which strategy close the position.
                # print(f"Position closed by strategy: {strategy.__class__.__name__}")
                self.position.close()
                return
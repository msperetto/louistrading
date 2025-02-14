from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from backtesting import Backtest, Strategy
from backtesting.lib import resample_apply
from main.common.strategybuy import StrategyBuy
from main.common.strategysell import StrategySell
from main.common.trendanalysis import TrendAnalysis
from main.common.strategyLong import StrategyLong
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
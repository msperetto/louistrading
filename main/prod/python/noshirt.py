import time
from common.python.filter import *
from common.python.trigger import *
from common.python.trade import *
from common.python.trend import *
from common.python.strategybuy import StrategyBuy
from common.python.strategysell import StrategySell
from common.python.trendanalysis import TrendAnalysis
from prod.python.indicators import Indicators
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.python.strategy import *

#todo 

class NoShirt():

    def __init__(self, dataset, strategy_long=None, strategy_short=None):

        self.dataset = dataset
        self.indicators = Indicators()
        self.strategy_long = strategy_long
        self.strategy_short = strategy_short
        
        self.classes = {}

        #instantiating buying support objects
        # exec(self.filter_buy_class)
        # exec(self.trigger_buy_class)
        # exec(self.trade_buy_class)
        # exec(self.trend_class)

        # #adding classes name to stats list to populate DB
        # self.classes['filter_buy'] = self.filterBuy.__class__.__name__
        # self.classes['trigger_buy'] = self.triggerBuy.__class__.__name__
        # self.classes['trade_buy']= self.tradeBuy.__class__.__name__
        # self.classes['trend'] = self.trend.__class__.__name__

        # #instantiating selling support objects
        # exec(self.filter_sell_class)
        # exec(self.trigger_sell_class)
        # exec(self.trade_sell_class)
        
        # #adding classes name to stats list to populate DB
        # self.classes['filter_sell'] = self.filterSell.__class__.__name__
        # self.classes['trigger_sell'] = self.triggerSell.__class__.__name__
        # self.classes['trade_sell'] = self.tradeSell.__class__.__name__


        # #instantiating buying and selling strategy classes
        # self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        # self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)
        # self.trendAnalysis = TrendAnalysis(self.trend)

    def update_dataset(self):
        #dataframes with indicators
        if self.strategy_long:
            self.long_df = self.prepare_indicators(self.strategy_long, self.dataset)
        
        if self.strategy_short:
            self.short_df = self.prepare_indicators(self.strategy_short, self.dataset)


    def prepare_indicators(self, strategy, dataset):
        indicator_df = Indicators()
        indicator_df.strategy.ta.remove({})
        indicators_list = []

        try:
            indicators_list.append({"kind": "ema", "length": strategy.ema_p_short}) 
        except AttributeError:
            pass

        try:
            indicators_list.append({"kind": "ema", "length": strategy.ema_p_medium}) 
        except AttributeError:
            pass

        try:
            indicators_list.append({"kind": "ema", "length": strategy.ema_p_long}) 
        except AttributeError:
            pass

        try:
            indicators_list.append({"kind": "sma", "length": strategy.sma_p_short}) 
        except AttributeError:
            pass

        try:
            indicators_list.append({"kind": "sma", "length": strategy.sma_p_medium}) 
        except AttributeError:
            pass

        try:
            indicators_list.append({"kind": "sma", "length": strategy.sma_p_long}) 
        except AttributeError:
            pass

        try:
            indicators_list.append({"kind": "rsi", "length": strategy.rsi_period}) 
        except AttributeError:
            pass

        for indicator in indicators_list:
            indicator_df.add_indicator_to_strategy(indicator)
            
        indicator_df.apply_strategy_to_df(dataset)

        return indicator_df
    
    def update_indicators(self, strategy):
        try:
            self.ema_short = self.dataset[f"EMA_{strategy.ema_p_short}"].values.tolist()
        except AttributeError:
            pass

        try:
            self.ema_medium = self.dataset[f"EMA_{strategy.ema_p_medium}"].values.tolist()
        except AttributeError:
            pass

        try:
            self.ema_long = self.dataset[f"EMA_{strategy.ema_p_long}"].values.tolist()
        except AttributeError:
            pass

        try:
            self.sma_short = self.dataset[f"SMA_{strategy.sma_p_short}"].values.tolist()
        except AttributeError:
            pass

        try:
            self.sma_medium = self.dataset[f"SMA_{strategy.sma_p_medium}"].values.tolist()
        except AttributeError:
            pass

        try:
            self.sma_long = self.dataset[f"SMA_{strategy.sma_p_long}"].values.tolist()
        except AttributeError:
            pass

        try:
            self.rsi = self.dataset[f"RSI_{strategy.rsi_period}"].values.tolist()
        except AttributeError:
            pass


    def evaluate_last_candle(self):
        if self.stop_loss:
            stop_loss = self.data.Close[-1] * ((100-self.stop_loss)/100)
        else: stop_loss = None
        if self.take_profit:
            take_profit = self.data.Close[-1] * ((100+self.take_profit)/100)
        else: take_profit = None

        if self.trendAnalysis.is_upTrend():
            if self.strategyBuy.shouldBuy(): self.buy(sl=stop_loss, tp=take_profit)
        else:
            #keeps updating trigger status even if not on trend
            self.strategyBuy.triggeredState.isStillValid()

        if self.strategySell.shouldSell(): self.position.close()


import time
from common.python.filter import *
from common.python.trigger import *
from common.python.trade import *
from common.python.trend import *
from common.python.strategybuy import StrategyBuy
from common.python.strategysell import StrategySell
from common.python.trendanalysis import TrendAnalysis
from common.python import management
from prod.python.dataset import Dataset
from prod.python.negociate import Negociate
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd
from time import sleep
from common.python.strategy import *


# strategy manager 
class NoShirt():

    #modificar aqui para ser somente uma estratégia
    def __init__(self, pair, intraday_ohcl_df, trend_ohcl_df, api_id, api_key, order_value, strategy, stop_loss = None, take_profit = None):

        self.pair = pair
        self.intraday_dataset = intraday_ohcl_df #dataframe containing only ohcl data, with no indicators
        self.trend_dataset = trend_ohcl_df
        self.api_id = api_id
        self.api_key = api_key
        self.order_value = order_value
        self.strategy = strategy
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.negociate = Negociate(self.pair, self.api_id, self.api_key)
        
        self.classes = {}

            # run everything necessary to the strategy evaluation for the last candle.
    def run(self):
        self.update_dataset(self.intraday_dataset, "intraday")
        trend_indicator_list = self.update_dataset(self.trend_dataset, "trend")

        self.complete_dataset = management.merge_dataframes(self.intraday_dataset, self.trend_dataset, *trend_indicator_list)
        self.update_indicators(self.strategy)


        #modificar aqui para ser apenas 1 estratégia
        self.set_support_objects(self.strategy)

        self.evaluate_last_candle()

    # instantiating objects for filter, trigger, trade e trend classes
    def set_support_objects(self, strategy):
        exec(strategy.filter_buy_class)
        exec(strategy.trigger_buy_class)
        exec(strategy.trade_buy_class)
        exec(strategy.trend_class)

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.filterBuy.__class__.__name__
        self.classes['trigger_buy'] = self.triggerBuy.__class__.__name__
        self.classes['trade_buy']= self.tradeBuy.__class__.__name__
        self.classes['trend'] = self.trend.__class__.__name__

        #instantiating selling support objects
        exec(strategy.filter_sell_class)
        exec(strategy.trigger_sell_class)
        exec(strategy.trade_sell_class)
        
        #adding classes name to stats list to populate DB
        self.classes['filter_sell'] = self.filterSell.__class__.__name__
        self.classes['trigger_sell'] = self.triggerSell.__class__.__name__
        self.classes['trade_sell'] = self.tradeSell.__class__.__name__

        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)
        self.trendAnalysis = TrendAnalysis(self.trend)


    def update_dataset(self, dataset, period_type):
        #dataset with indicators
        #period type can be intraday or trend
        self.prepare_indicators(dataset, self.strategy, period_type) #df containing ochl + indicators
                    

    # get the ohlc df and add the indicators columns to it
    def prepare_indicators(self, dataset, strategy, period_type):
        indicator_df = Dataset()
        indicator_df.strategy.ta.remove({})
        indicators_list = []

        if period_type == 'intraday':
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

        elif period_type == 'trend':
            try:
                indicators_list.append({"kind": "ema", "length": strategy.ema_trend_short}) 
            except AttributeError:
                pass

            try:
                indicators_list.append({"kind": "sma", "length": strategy.sma_trend_medium}) 
            except AttributeError:
                pass

            try:
                indicators_list.append({"kind": "sma", "length": strategy.sma_trend_long}) 
            except AttributeError:
                pass

        for indicator in indicators_list:
            indicator_df.add_indicator_to_strategy(indicator)
            
        #here the dataset will be updated
        indicator_df.apply_strategy_to_df(dataset)

        return [indicator['kind']+'_'+str(indicator['length']) for indicator in indicators_list]
    
    # Isolates every indicator in separeted attributes
    # period_type can be intraday or trend
    def update_indicators(self, strategy, period_type):

        if period_type == 'intraday': 
            try:
                self.ema_short = self.complete_dataset[f"EMA_{strategy.ema_p_short}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.ema_medium = self.complete_dataset[f"EMA_{strategy.ema_p_medium}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.ema_long = self.complete_dataset[f"EMA_{strategy.ema_p_long}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.sma_short = self.complete_dataset[f"SMA_{strategy.sma_p_short}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.sma_medium = self.complete_dataset[f"SMA_{strategy.sma_p_medium}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.sma_long = self.complete_dataset[f"SMA_{strategy.sma_p_long}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.rsi = self.complete_dataset[f"RSI_{strategy.rsi_period}"].values.tolist()
                self.rsi_layer_cheap = strategy.rsi_layer_cheap
                self.rsi_layer_expensive = strategy.rsi_layer_expensive
            except AttributeError:
                pass
        
        elif period_type == 'trend':
            try:
                self.ema_trend_short = self.complete_dataset[f"EMA_{strategy.ema_trend_short}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.sma_trend_medium = self.complete_dataset[f"SMA_{strategy.sma_trend_medium}"].values.tolist()
            except AttributeError:
                pass

            try:
                self.sma_trend_long = self.complete_dataset[f"SMA_{strategy.sma_trend_long}"].values.tolist()
            except AttributeError:
                pass


    # check if can open position
    def try_open_position(self):
        if self.trendAnalysis.is_upTrend():
            if self.strategyBuy.shouldBuy():
                self.open_position_strategy = db.get_strategy_id(strategy.__class__.__name__)
                self.negociate.open_position("long", self.order_value, self.open_position_strategy)
        else:
            #keeps updating trigger status even if not on trend
            #verificar necessidade dessa atualização
            self.strategyBuy.triggeredState.isStillValid()
        

    def try_close_position(self):
        if self.strategySell.shouldSell(): 
            #checar aqui possibilidade de fechar a ordem completamente, ao invés de passar um valor
            self.negociate.close_position("long", self.order_value, self.open_position_strategy)



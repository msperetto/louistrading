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
from time import sleep
from common.python.strategy import *
from common.python.indicators_catalog import indicators_catalog

# strategy manager 
class StrategyManager():

    #modificar aqui para ser somente uma estratégia
    def __init__(self, pair, dataset, api_id, api_key, order_value, strategy, stop_loss = None, take_profit = None):

        self.pair = pair
        self.data = dataset
        self.api_id = api_id
        self.api_key = api_key
        self.order_value = order_value
        self.strategy = strategy
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.negociate = Negociate(self.pair, self.api_id, self.api_key)
        self.classes = {}
        self.set_support_objects()

    # run everything necessary to the strategy evaluation for the last candle.
    def run(self):
        self.try_open_position()

    def set_support_objects(self):
        # setting all attributes necessary depending on indicators utilized by the strategy
        for attr, config in indicators_catalog.items():
            try:
                column_name = f"{config['prefix'].upper()}_{getattr(self.strategy, attr)}"
                #adding prefix trend when looping the trend columns
                if config['period_type'] == 'trend':
                    column_name = f"TREND_{column_name}"
                setattr(self, attr, self.data[column_name])

                # creating attributes when the indicator has more information, like rsi, for example
                # number 3 here is the position in config dictionary where new attributes starts
                if len(config) > 3:
                    new_attrs = list(config.items())[3:]
                    for new_attr, attr_value in new_attrs:
                        setattr(self, attr_value, getattr(self.strategy, attr_value))
            except AttributeError:
                pass

        #setting max candles attributes:
        if getattr(self.strategy, 'intraday_max_candles_buy'):
            self.intraday_max_candles_buy = getattr(self.strategy, 'intraday_max_candles_buy')
        if getattr(self.strategy, 'intraday_max_candles_sell'):
            self.intraday_max_candles_sell = getattr(self.strategy, 'intraday_max_candles_sell')


        # instantiating objects for filter, trigger, trade e trend classes
        exec(self.strategy.filter_buy_class)
        exec(self.strategy.trigger_buy_class)
        exec(self.strategy.trade_buy_class)
        exec(self.strategy.trend_class)

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.filterBuy.__class__.__name__
        self.classes['trigger_buy'] = self.triggerBuy.__class__.__name__
        self.classes['trade_buy']= self.tradeBuy.__class__.__name__
        self.classes['trend'] = self.trend.__class__.__name__

        #instantiating selling support objects
        exec(self.strategy.filter_sell_class)
        exec(self.strategy.trigger_sell_class)
        exec(self.strategy.trade_sell_class)
        
        #adding classes name to stats list to populate DB
        self.classes['filter_sell'] = self.filterSell.__class__.__name__
        self.classes['trigger_sell'] = self.triggerSell.__class__.__name__
        self.classes['trade_sell'] = self.tradeSell.__class__.__name__

        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)
        self.trendAnalysis = TrendAnalysis(self.trend)


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



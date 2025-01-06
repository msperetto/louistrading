import time
from common.enums import *
from common.filter import *
from common.trigger import *
from common.trade import *
from common.trend import *
from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis
from common import management
from common.dao import strategy_dao
from prod.dataset import Dataset
from prod.negociate import Negociate
from backtesting.lib import resample_apply
import pandas_ta as ta
from time import sleep
from common.strategy import *
from common.indicators_catalog import indicators_catalog

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
        if hasattr(self.strategy, 'intraday_max_candles_buy'):
            self.intraday_max_candles_buy = getattr(self.strategy, 'intraday_max_candles_buy')
        if hasattr(self.strategy, 'intraday_max_candles_sell'):
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
                strategy = strategy_dao.get_strategy_by_name(self.strategy.__class__.__name__)
                self.negociate.open_position(Side_Type.LONG, self.order_value, strategy.id)
        else:
            #keeps updating trigger status even if not on trend
            #verificar necessidade dessa atualização
            self.strategyBuy.triggeredState.isStillValid()
        

    def try_close_position(self, strategy, trade_id):
        if self.strategySell.shouldSell(): 
            #checar aqui possibilidade de fechar a ordem completamente, ao invés de passar um valor
            self.negociate.close_position(Side_Type.LONG, self.order_value, strategy, trade_id)



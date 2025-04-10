import time
from common.enums import *
from common.filter import *
from common.strategyLong import StrategyLong
from common.strategyShort import StrategyShort
from common.trigger import *
from common.trade import *
from common.trend import *
from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis
from common import management
from common.dao import strategy_dao
from common.util import get_side
from prod.dataset import Dataset
from prod.negotiate import Negotiate
from backtesting.lib import resample_apply
import pandas_ta as ta
from time import sleep
from common.strategy import *
from common.indicators_catalog import indicators_catalog

class StrategyManager():

    #modificar aqui para ser somente uma estratégia
    def __init__(self, pair, pair_precision, dataset, api_id, api_key, order_value, strategy, stop_loss = None, take_profit = None):
        self.pair = pair
        self.pair_precision = pair_precision
        self.data = dataset
        self.api_id = api_id
        self.api_key = api_key
        self.order_value = order_value
        self.strategy = strategy
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.negotiate = Negotiate(self.pair, self.pair_precision, self.api_id, self.api_key)
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

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.strategy.filter_buy_class
        self.classes['trigger_buy'] = self.strategy.trigger_buy_class
        self.classes['trade_buy']= self.strategy.trade_buy_class
        self.classes['trend'] = self.strategy.trend_class
        self.classes['filter_sell'] = self.strategy.filter_sell_class
        self.classes['trigger_sell'] = self.strategy.trigger_sell_class
        self.classes['trade_sell'] = self.strategy.trade_sell_class

        # getting all class attributes to pass to buying and selling support objects
        self.attributes = {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not isinstance(getattr(self, attr), (type(self.set_support_objects), type(self.__init__)))}

        self.strategy.build_strategy_buy(
            self.strategy.filter_buy_class,
            self.strategy.trigger_buy_class,
            self.strategy.trade_buy_class,
            self.attributes,
            self
        )

        self.strategy.build_strategy_sell(
            self.strategy.filter_sell_class,
            self.strategy.trigger_sell_class,
            self.strategy.trade_sell_class,
            self.attributes,
            self
        )

        self.strategy.build_trend_analysis(
            self.strategy.trend_class,
            self.attributes,
            self
        )

        #instantiating buying support objects
        self.filterBuy = Filter().filter_factory(self.strategy.filter_buy_class, self, **self.attributes)
        self.triggerBuy = TriggeredState().trigger_factory(self.strategy.trigger_buy_class, self, **self.attributes)
        self.tradeBuy = Trade().trade_factory(self.strategy.trade_buy_class, self, **self.attributes)
        self.trend = Trend().trend_factory(self.strategy.trend_class, self, **self.attributes)

        
        #instantiating selling support objects
        self.filterSell = Filter().filter_factory(self.strategy.filter_sell_class, self, **self.attributes)
        self.triggerSell = TriggeredState().trigger_factory(self.strategy.trigger_sell_class, self, **self.attributes)
        self.tradeSell = Trade().trade_factory(self.strategy.trade_sell_class, self, **self.attributes)
       
        #instantiating buying and selling strategy classes
        self.strategyBuy = StrategyBuy(self.filterBuy, self.triggerBuy, self.tradeBuy)
        self.strategySell = StrategySell(self.filterSell, self.triggerSell, self.tradeSell)
        self.trendAnalysis = TrendAnalysis(self.trend)


    # check if can open position
    def try_open_position(self):
        # Gets the Side_Type.LONG or Side_Type.SHORT based on the strategy type.
        side = get_side(self.strategy)
        if side is None: return False

        if self.strategy.shouldOpen(): 
            strategy = strategy_dao.get_strategy_by_name(self.strategy.__class__.__name__)
            return self.negotiate.open_position(side, self.order_value, strategy.id)
        return False

    def try_close_position(self, strategy, trade_id):
        # Gets the Side_Type.LONG or Side_Type.SHORT based on the strategy type.
        side = get_side(self.strategy) 
        if side is None: return False

        if self.strategy.shouldClose():
            return self.negotiate.close_position(side, self.order_value, strategy, trade_id)
        return False
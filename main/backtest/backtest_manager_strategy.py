from common.util import import_all_strategies
from common import STRATEGIES_PATH_BT, STRATEGIES_MODULE_BT
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
from common.strategyLong import StrategyLong
from common.strategyShort import StrategyShort

# It deals with a single strategy (passed as a parameter) 
class BacktestManagerStrategy(Strategy):
    # Import all strategies from the strategies folder.
    import_all_strategies(STRATEGIES_PATH_BT, STRATEGIES_MODULE_BT, globals())

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
    trend_class = "UpTrend_alwaysTrue"
    filter_buy_class = "Filter_alwaysTrue"
    trigger_buy_class = "TriggeredState_alwaysTrue"
    trade_buy_class = "TradeBuy_HighLastCandle"
    filter_sell_class = "Filter_alwaysTrue"
    trigger_sell_class = "TriggeredState_alwaysTrue"
    trade_sell_class = "TradeSell_LowLastCandle"
    strategy_buy = None
    strategy_sell = None
    trend_analysis = None
    strategy_class = None

    def init(self):
        self.classes = {}

        # creating indicators series (1 indicator value for each candle)
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

        # TODO: Understand why the import_all_strategies() function is not working properly
        # import_all_strategies()

        self.strategy = globals().get(self.strategy_class)()

        #adding classes name to stats list to populate DB
        self.classes['filter_buy'] = self.strategy.filter_buy_class
        self.classes['trigger_buy'] = self.strategy.trigger_buy_class
        self.classes['trade_buy']= self.strategy.trade_buy_class
        self.classes['trend'] = self.trend_class
        self.classes['filter_sell'] = self.strategy.filter_sell_class
        self.classes['trigger_sell'] = self.strategy.trigger_sell_class
        self.classes['trade_sell'] = self.strategy.trade_sell_class

        #getting all class attributes to pass to buying and selling support objects
        self.attributes = {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not isinstance(getattr(self, attr), type(self.init))}

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
            self.trend_class,
            self.attributes,
            self
        )
                
    def next(self):
        self.try_open_position()
        self.try_close_position()
         
    # try open position
    def try_open_position(self):
        if isinstance(self.strategy, StrategyLong):
            stop_loss = self.calculate_stop_loss()
            take_profit = self.calculate_take_profit()
            if self.strategy.shouldOpen():
                self.buy(sl=stop_loss, tp=take_profit)
                return
        elif isinstance(self.strategy, StrategyShort):
            stop_loss = self.calculate_stop_loss(is_short=True)
            take_profit = self.calculate_take_profit(is_short=True)
            if self.strategy.shouldOpen():
                self.sell(sl=stop_loss, tp=take_profit)
                return

    # try close position
    def try_close_position(self):
        if not self.position:
            # In case there's no opened position, just skip the logic. 
            return

        if self.strategy.shouldClose():
            self.position.close()
            return
        
    def calculate_stop_loss(self, is_short=False):
        """
        Calcula o Stop Loss. Para operações SHORT, o Stop Loss deve ser acima do preço de entrada.
        """
        if self.stop_loss:
            if is_short:
                return self.data.Close[-1] * ((100 + self.stop_loss) / 100)  # Para SHORT, Stop Loss é para cima
            else:
                return self.data.Close[-1] * ((100 - self.stop_loss) / 100)  # Para LONG, Stop Loss é para baixo
        return None

    def calculate_take_profit(self, is_short=False):
        """
        Calcula o Take Profit. Para operações SHORT, o Take Profit deve ser abaixo do preço de entrada.
        """
        if self.take_profit:
            if is_short:
                return self.data.Close[-1] * ((100 - self.take_profit) / 100)  # Para SHORT, Take Profit é para baixo
            else:
                return self.data.Close[-1] * ((100 + self.take_profit) / 100)  # Para LONG, Take Profit é para cima
        return None
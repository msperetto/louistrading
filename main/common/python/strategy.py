from common.python import database_operations as db
from common.python.strategylong import StrategyLong

class Strategy_Test():
    def __init__(self, optimize: bool = False):
        self.intraday_ema_short = 8
        self.intraday_sma_long = 44
        self.trend_sma_short = 7

        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.trend_longest_indicator_value = 44
        self.filter_buy_class=db.get_class_code("FilterBuy_EMAshort_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_Price_gt_EMAshort")
        self.trend_class=db.get_class_code("UpTrend_AlwaysTrend")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_B1():
    def __init__(self, optimize: bool = False):
        if not optimize:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 44
            self.intraday_sma_short = 7
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 48
            self.intraday_ema_short = 9
            self.intraday_rsi_layer_cheap = 19
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.intraday_max_candles_buy = 4
            self.intraday_max_candles_sell = 5
        else:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 44
            self.intraday_sma_short = 7
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 48
            self.intraday_ema_short = 9
            self.intraday_rsi_layer_cheap = 19
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi_period = 4
            self.intraday_max_candles_buy = 4
            self.intraday_max_candles_sell = 5

        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.trend_longest_indicator_value = 44
        self.filter_buy_class=db.get_class_code("FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.trend_class=db.get_class_code("UpTrend_AlwaysTrend")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_B2():
    def __init__(self, optimize: bool = False):
        if not optimize:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = 7
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = 9
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5
        else:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = range(7, 9, 1)
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = range(6, 10, 1)
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5
        
        self.intraday_interval = "h"
        self.trend_interval = "D"
        self.filter_buy_class=db.get_class_code("FilterBuy_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")
       

class Strategy_B3():
    def __init__(self, optimize: bool = False):
        if not optimize:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = 7
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = 9
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5
        else:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = range(7, 9, 1)
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = range(6, 10, 1)
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5

        self.intraday_interval = "h"
        self.trend_interval = "D"
        self.filter_buy_class=db.get_class_code("FilterBuy_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")


class Strategy_C1():
    def __init__(self, optimize: bool = False):
        if not optimize:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = 9
            self.sma_p_medium = 20
            self.sma_p_long = 48
            self.ema_p_short = 8
            self.rsi_layer_cheap = 22
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 5
            self.max_candles_sell = 5
        else:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = 7
            self.sma_p_medium = 20
            self.sma_p_long = 48
            self.ema_p_short = 8
            self.rsi_layer_cheap = 22
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 5
            self.max_candles_sell = 5

        self.intraday_interval = "h"
        self.trend_interval = "D"
        self.filter_buy_class=db.get_class_code("FilterBuy_RSI")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

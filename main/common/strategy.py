from common.dao import database_operations as db

class Strategy_Test():
    def __init__(self, optimize: bool = False):
        self.intraday_ema_short = 2
        self.intraday_sma_long = 44
        self.trend_sma_short = 7

        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.trend_longest_indicator_value = 44
        self.filter_buy_class=db.get_class_code("FilterBuy_alwaysTrue")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_Price_gt_EMAshort")
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
            self.intraday_rsi = 4
            self.intraday_max_candles_buy = 4
            self.intraday_max_candles_sell = 5

        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.trend_longest_indicator_value = 44
        self.filter_buy_class=db.get_class_code("FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")
        self.trend_class=db.get_class_code("UpTrend_AlwaysTrend")

class Strategy_B2():
    def __init__(self, optimize: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = 9
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 51
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = range(48,52,1)
            self.intraday_ema_short = range(7,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = 51
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.filter_buy_class=db.get_class_code("FilterBuy_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")
        self.trend_class=db.get_class_code("UpTrend_Price_gt_SMAlong")
       
class Strategy_B3():
    def __init__(self, optimize: bool = False):
        if not optimize:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 44
            self.adx_trend_layer = 25
            self.intraday_sma_short = 7
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 48
            self.intraday_ema_short = 9
            self.intraday_rsi_layer_cheap = 19
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.intraday_max_candles_buy = 4
            self.intraday_max_candles_sell = 4
            self.trend_longest_indicator_value = 44
        else:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 44
            self.adx_trend_layer = 25
            self.intraday_sma_short = range(7, 9, 1)
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 48
            self.intraday_ema_short = range(6, 10, 1)
            self.intraday_rsi_layer_cheap = 19
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.intraday_max_candles_buy = 4
            self.intraday_max_candles_sell = 4
            self.trend_longest_indicator_value = 44

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
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 44
            self.adx_trend_layer = 25
            self.intraday_sma_short = 9
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 48
            self.intraday_ema_short = 8
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.intraday_max_candles_buy = 5
            self.intraday_max_candles_sell = 5
            self.trend_longest_indicator_value = 44
        else:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 44
            self.adx_trend_layer = 25
            self.intraday_sma_short = 9
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 48
            self.intraday_ema_short = 8
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.intraday_max_candles_buy = 5
            self.intraday_max_candles_sell = 5
            self.trend_longest_indicator_value = 44

        self.intraday_interval = "h"
        self.trend_interval = "D"
        self.filter_buy_class=db.get_class_code("FilterBuy_RSI")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

from common.dao import database_operations as db

class Strategy_Test():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        self.intraday_ema_short = 2
        self.intraday_sma_long = 44
        self.trend_sma_short = 7

        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.trend_longest_indicator_value = 44
        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Price_gt_EMAshort"
        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_EMAshort"
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_AlwaysTrend"

class Strategy_B1():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
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
        self.filter_buy_class = "FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong"
        self.trigger_buy_class = "TriggeredState_MaxCandles_Buy"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"
        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_EMAshort"
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_AlwaysTrend"

class Strategy_B2():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
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
        self.filter_buy_class = "FilterBuy_SMAmedium_gt_SMAlong"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"
        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_EMAshort"
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_SMAlong"

class Strategy_Short_Test1():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.intraday_ema_short = 9
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 51
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            self.intraday_rsi_layer_cheap = range(22, 23, 1)
            self.intraday_rsi_layer_expensive = range(79, 80, 1)
            self.intraday_rsi = range(3, 7, 1)
            self.trend_longest_indicator_value = 10
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Price_EMAshort"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_SMAlong"

class Strategy_S1():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = 9
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 51
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong_Price_lt_SMAlong"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_AlwaysTrend"

class Strategy_S6():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 9
            self.trend_sma_medium = 20
            self.trend_sma_long = 50
            self.intraday_ema_short = 9
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 51
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_lt_SMAmedium"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Price_EMAshort"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_AlwaysTrend"
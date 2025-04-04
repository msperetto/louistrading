from common.dao import database_operations as db

#------------------------------------------------------
# LONG strategies:

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
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"
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
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"
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
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_SMAlong"

class Strategy_L1A():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_Low_lt_LowLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_L1B():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_L1C():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_High_lt_HighLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_EMAshort"

class Strategy_L1CX():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_High_lt_HighLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_SMAmedium_lt_SMAlong"

class Strategy_L1D():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_LowLastCandle_EMAshort_lt_SMAmedium"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_L2():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 21
            self.trend_sma_long = 50
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 18
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 78
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap =  range(5, 17, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 6, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAlong"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_Low_lt_LowLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_AlwaysTrend"

class Strategy_L3():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 21
            self.trend_sma_long = 50
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 18
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 78
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap =  range(5, 17, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 6, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_High_lt_HighLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_AlwaysTrend"

class Strategy_L4A():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAmedium"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_Low_lt_LowLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_L4B():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAmedium"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_L4C():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAmedium"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_High_lt_HighLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_EMAshort"


class Strategy_L4CX():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAmedium"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_High_lt_HighLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_SMAmedium_lt_SMAlong"

class Strategy_L4D():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 14
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,9,1)
            self.trend_sma_medium = range(18,21,1)
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAmedium"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_LowLastCandle_EMAshort_lt_SMAmedium"
        
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"


class Strategy_L5():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 21
            self.trend_sma_long = 50
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 18
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 78
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = range(48,50,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,50,1)
            self.intraday_rsi_layer_cheap =  range(13, 16, 1)
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = range(3, 4, 1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_buy_class = "FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium_Low_lt_LowLastCandle"
        
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_AlwaysTrend"

#------------------------------------------------------
# SHORT strategies:

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
        self.trade_buy_class = "TradeBuy_Price_gt_EMAshort"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_SMAlong"

class Strategy_S1():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 20
            self.trend_sma_long = 48
            self.intraday_ema_short = 10
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 51
            self.trend_longest_indicator_value = 51
            self.stop_loss = 3
            self.take_profit = 1
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            # self.stop_loss = range(1,5,1)
            # self.take_profit = range(1,5,1)

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
            self.trend_class = "DownTrend_EMAshort_lt_SMAmedium_lt_SMAlong"

class Strategy_S6():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 7
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = 6
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
            # self.stop_loss = range(1,5,1)
            # self.take_profit = range(1,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_lt_SMAmedium"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Price_gt_EMAshort"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_EMAshort"

class Strategy_S7():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 7
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 7
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 50
            self.stop_loss = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)     
            self.stop_loss = range(1,5,1)
            # self.take_profit = range(1,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong_Price_lt_SMAmedium"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Close_gt_CloseLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_EMAshort_lt_SMAmedium"

class Strategy_SH1():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 82
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,8,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Close_gt_CloseLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_alwaysTrend"

class Strategy_SH2():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 7
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = 7
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 51
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 3
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

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAlong"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_EMAshort_lt_SMAmedium"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_alwaysTrend"

class Strategy_SH3():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 7
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 11
            self.intraday_sma_medium = 18
            self.intraday_sma_long = 51
            # self.intraday_rsi_layer_cheap = 22
            # self.intraday_rsi_layer_expensive = 79
            # self.intraday_rsi = 3
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

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong_Price_lt_SMAmedium"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAlong"

class Strategy_SH4():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,8,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_SH5():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 48
        else:
            self.trend_ema_short = range(6,8,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_SH6():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 7
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = 7
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 51
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,8,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI_price_x_SMAmedium"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_alwaysTrend"
    
class Strategy_SH7():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 19
            self.trend_sma_long = 48
            self.intraday_ema_short = 8
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 49
            self.stop_loss = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            self.stop_loss = range(1,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_SH8():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 19
            self.trend_sma_long = 48
            self.intraday_ema_short = 8
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 49
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 3
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
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_SH9():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 19
            self.trend_sma_long = 48
            self.intraday_ema_short = 8
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 49
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 3
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

        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong_Price_lt_SMAmedium"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"

class Strategy_SC1():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 77
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_SMAlong"

class Strategy_SC1A():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 77
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_EMAshort"

class Strategy_SC1B():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 76
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_EMAshort_gt_SMAmedium"

class Strategy_SC1C():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 21
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_SMAmedium_gt_SMAlong"

class Strategy_SC2():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 75
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Price_gt_EMAshort"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_SMAmedium_lt_SMAlong"

class Strategy_SC3():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 75
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Close_lt_CloseLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_EMAshort_lt_SMAmedium"   

class Strategy_SC4():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 50
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 75
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_Price_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_SMAmedium_lt_SMAlong"

class Strategy_SC5():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 17
            self.intraday_sma_long = 50
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 76
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_SMAmedium_lt_SMAlong"

class Strategy_SC6():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 50
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 76
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_SMAmedium_lt_SMAlong"

class Strategy_SC6A():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 8
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 50
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 79
            self.intraday_rsi = 3
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_EMAshort_gt_SMAmedium"

class Strategy_SC6B():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 48
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 21
            self.intraday_sma_long = 50
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 75
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_EMAshort"

class Strategy_SC6C():
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 21
            self.trend_sma_long = 50
            self.intraday_ema_short = 6
            self.intraday_sma_medium = 18
            self.intraday_sma_long = 48
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 78
            self.intraday_rsi = 4
            self.trend_longest_indicator_value = 51
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,11,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,51,1)
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = range(75,81,1)
            self.intraday_rsi = range(3,5,1)
            self.trend_longest_indicator_value = 51
        
        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_SMAmedium_gt_SMAlong"
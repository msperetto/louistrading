import database_operations as db

class Strategy_Test():
    def __init__(self, optimize: bool = True):
        pass

class Strategy_B1():
    def __init__(self, optimize: bool = True):
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

        self.filter_buy_class=db.get_class_code("FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_B2():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = 9
            self.sma_p_medium = 19
            self.sma_p_long = 51
        else:
            self.ema_trend_short = range(6, 10, 1)
            self.sma_trend_medium = range(18, 22, 1)
            self.sma_trend_long = range(48, 52, 1)
            self.adx_trend_layer = 25
            self.ema_p_short = range(6, 10, 1)
            self.sma_p_medium = range(18, 22, 1)
            self.sma_p_long = range(48, 52, 1)

        self.filter_buy_class=db.get_class_code("FilterBuy_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")
       

class Strategy_B3():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 8
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = 7
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = 9
        else:
            self.ema_trend_short = 8
            self.sma_trend_medium = range(18, 22, 1)
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_short = range(7, 9, 1)
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = range(6, 10, 1)

        self.filter_buy_class=db.get_class_code("FilterBuy_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_B4():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 9
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = 9
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5
        else:
            self.ema_trend_short = range(6, 10, 1)
            self.sma_trend_medium = range(18, 22, 1)
            self.sma_trend_long = range(48, 52, 1)
            self.adx_trend_layer = 25
            self.sma_p_medium = range(18, 22, 1)
            self.sma_p_long = range(48, 52, 1)
            self.ema_p_short = range(6, 10, 1)
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5

        self.filter_buy_class=db.get_class_code("FilterBuy_EMAshort_gt_SMAmedium")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_B5():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 9
            self.sma_trend_medium = 18
            self.sma_trend_long = 44
            self.adx_trend_layer = 25
            self.sma_p_medium = 19
            self.sma_p_long = 48
            self.ema_p_short = 9
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5
        else:
            self.ema_trend_short = range(6, 10, 1)
            self.sma_trend_medium = range(18, 22, 1)
            self.sma_trend_long = range(48, 52, 1)
            self.adx_trend_layer = 25
            self.sma_p_medium = range(18, 22, 1)
            self.sma_p_long = range(48, 52, 1)
            self.ema_p_short = range(6, 10, 1)
            self.rsi_layer_cheap = 19
            self.rsi_layer_expensive = 79
            self.rsi_period = 4
            self.max_candles_buy = 4
            self.max_candles_sell = 5            

        self.filter_buy_class=db.get_class_code("FilterBuy_EMAshort_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_C1():
    def __init__(self, optimize: bool = True):
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

        self.filter_buy_class=db.get_class_code("FilterBuy_RSI")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_X1():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = 8
            self.sma_p_medium = 19
            self.sma_p_long = 51
            self.max_candles_buy = 22  #17, 22
            self.rsi_period = 4
            self.rsi_layer_cheap = 23
            self.rsi_layer_expensive = 90
        else:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = range(6, 12, 1)
            self.sma_p_medium = 19
            self.sma_p_long = 51
            self.max_candles_buy = range(2, 30, 1)
            self.rsi_period = range(3, 10, 1)
            self.rsi_layer_cheap = range(10, 25, 1)
            self.rsi_layer_expensive = 90

        self.filter_buy_class=db.get_class_code("FilterBuy_RSI")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_Price_gt_EMAshort")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_X2():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = 10
            self.sma_p_medium = 19
            self.sma_p_long = 51
            self.max_candles_buy = 15 #15
            self.rsi_period = 5
            self.rsi_layer_cheap = 15
            self.rsi_layer_expensive = 90
        else:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = range(6, 12, 1)
            self.sma_p_medium = 19
            self.sma_p_long = 51
            self.max_candles_buy = range(3, 23, 1)
            self.rsi_period = range(3, 10, 1)
            self.rsi_layer_cheap = range(10, 24, 1)
            self.rsi_layer_expensive = 90

        self.filter_buy_class=db.get_class_code("FilterBuy_RSI_EMAshort_lt_SMAmedium_lt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_Price_gt_EMAshort")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

class Strategy_X3():
    def __init__(self, optimize: bool = True):
        if not optimize:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = 10
            self.sma_p_medium = 19
            self.sma_p_long = 51
            self.max_candles_buy = 15 #15
            self.rsi_period = 5
            self.rsi_layer_cheap = 15
            self.rsi_layer_expensive = 90
        else:
            self.ema_trend_short = 6
            self.sma_trend_medium = 18
            self.sma_trend_long = 50
            self.adx_trend_layer = 25
            self.ema_p_short = range(6, 12, 1)
            self.sma_p_medium = range(18, 21, 1)
            self.sma_p_long = 51
            self.max_candles_buy = range(3, 23, 1)
            self.rsi_period = range(3, 10, 1)
            self.rsi_layer_cheap = range(10, 24, 1)
            self.rsi_layer_expensive = 90

        self.filter_buy_class=db.get_class_code("FilterBuy_RSI_EMAshort_lt_SMAmedium_lt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredState_MaxCandles")
        self.trade_buy_class=db.get_class_code("TradeBuy_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")
import database_operations as db

class Strategy_B1():
    def __init__(self):
        self.sma_p_short = 7
        self.sma_p_medium = 19
        self.sma_p_long = 48
        self.ema_p_short = 9
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

class Strategy_C1():
    def __init__(self):
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

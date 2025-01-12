from common.dao import database_operations as db

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
        
        self.intraday_interval = "1h"
        self.trend_interval = "1d"
        self.filter_buy_class=db.get_class_code("FilterBuy_SMAmedium_gt_SMAlong")
        self.trigger_buy_class=db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class=db.get_class_code("TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium")
        self.filter_sell_class=db.get_class_code("FilterSell_alwaysTrue")
        self.trigger_sell_class=db.get_class_code("TriggeredStateSell_alwaysTrue")
        self.trade_sell_class=db.get_class_code("TradeSell_Price_EMAshort")

        self.trend_class=db.get_class_code("UpTrend_Price_gt_SMAlong")
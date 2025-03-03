from common.strategyShort import StrategyShort

class Strategy_Short_Test1(StrategyShort):
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = 9
            self.intraday_sma_medium = 19
            self.intraday_sma_long = 51
            self.intraday_rsi_layer_cheap = 22
            self.intraday_rsi_layer_expensive = 80
            self.intraday_rsi = 3
        else:
            self.trend_ema_short = 6
            self.trend_sma_medium = 18
            self.trend_sma_long = 50
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            self.intraday_rsi_layer_cheap = range(22, 23, 1)
            self.intraday_rsi_layer_expensive = range(79, 80, 1)
            self.intraday_rsi = range(3, 7, 1)
        
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

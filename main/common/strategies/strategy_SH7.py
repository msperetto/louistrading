from common.strategyShort import StrategyShort

class Strategy_SH7(StrategyShort):
    """
    SH7: Strategy Short - Tendência de baixa
    """    
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        super().__init__()
        # Define parameters for indicators
        if not optimize:
            self.trend_ema_short = 6
            self.trend_sma_medium = 19
            self.trend_sma_long = 48
            self.intraday_ema_short = 8
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 49
            self.stop_loss = 4
        else:
            self.trend_ema_short = range(6,11,1)
            self.trend_sma_medium = range(18,22,1)
            self.trend_sma_long = range(48,51,1)
            self.intraday_ema_short = range(6,12,1)
            self.intraday_sma_medium = range(18,22,1)
            self.intraday_sma_long = range(48,52,1)
            self.stop_loss = range(1,5,1)

        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        # Define components for strategy sell logic
        self.filter_sell_class = "FilterSell_EMAshort_lt_SMAmedium_lt_SMAlong"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_lt_EMAshort"

        # Define components for strategy buy logic
        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_EMAshort_gt_SMAmedium"

        # Define other strategy components
        if (shouldIncludeTrend):
            self.trend_class = "DownTrend_Price_lt_SMAmedium"
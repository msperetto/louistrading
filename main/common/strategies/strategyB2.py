from common.strategyLong import StrategyLong

class Strategy_B2(StrategyLong):
    """
    B2 strategy that configures the necessary components and indicator parameters.
    """

    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        super().__init__()
        # Define parameters for indicators
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


        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        # Define components for strategy buy logic
        self.filter_buy_class = "FilterBuy_SMAmedium_gt_SMAlong"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        # Define components for strategy sell logic
        self.filter_sell_class = "Filter_alwaysTrue"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Price_EMAshort"

        # Define other strategy components
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_Price_gt_SMAlong"
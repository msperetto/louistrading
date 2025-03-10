from common.strategyShort import StrategyShort

class Strategy_SC6A(StrategyShort):
    """
    SC1A: Strategy Short - Contra-Tendencia
    """    
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        super().__init__()
        # Define parameters for indicators
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

        self.intraday_interval = "2h"
        self.trend_interval = "1d"

        # Define components for strategy sell logic
        self.filter_sell_class = "FilterSell_RSI"
        self.trigger_sell_class = "TriggeredState_alwaysTrue"
        self.trade_sell_class = "TradeSell_Low_lt_LowLastCandle"

        # Define components for strategy buy logic
        self.filter_buy_class = "Filter_alwaysTrue"
        self.trigger_buy_class = "TriggeredState_alwaysTrue"
        self.trade_buy_class = "TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium"

        # Define other strategy components
        if (shouldIncludeTrend):
            self.trend_class = "UpTrend_EMAshort_gt_SMAmedium"
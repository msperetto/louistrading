from common.strategyShort import StrategyShort

class Strategy_SH7(StrategyShort):
    """
    SH7: Strategy Short - Tendência de baixa
    """    
    def __init__(self, optimize: bool = False, shouldIncludeTrend: bool = False):
        super().__init__()
        # Define parameters for indicators
        if not optimize:
            self.trend_sma_medium = 19
            self.intraday_ema_short = 8
            self.intraday_sma_medium = 20
            self.intraday_sma_long = 49
            self.stop_loss = 4
        
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
        self.trend_class = "DownTrend_Price_lt_SMAmedium"
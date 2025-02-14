from main.common.strategyLong import StrategyLong

class Strategy_B2(StrategyLong):
    """
    B2 strategy that configures the necessary components and indicator parameters.
    """

    def __init__(self, db):
        super().__init__()
        # Define parameters for indicators
        self.trend_ema_short = 6
        self.trend_sma_medium = 18
        self.trend_sma_long = 50
        self.intraday_ema_short = 9
        self.intraday_sma_medium = 19
        self.intraday_sma_long = 51

        self.intraday_interval = "1h"
        self.trend_interval = "1d"

        # Define components for strategy buy logic
        self.filter_buy_class = db.get_class_code("FilterBuy_SMAMedium_gt_SMALong")
        self.trigger_buy_class = db.get_class_code("TriggeredStateBuy_alwaysTrue")
        self.trade_buy_class = db.get_class_code("TradeBuy_Example")

        # Define components for strategy sell logic
        self.filter_sell_class = db.get_class_code("FilterSell_Example")
        self.trigger_sell_class = db.get_class_code("TriggeredStateSell_Example")
        self.trade_sell_class = db.get_class_code("TradeSell_Example")

        # Construct the strategy buy and sell logic using the base class methods
        self.strategy_buy = self.build_strategy_buy(
            self.filter_buy_class,
            self.trigger_buy_class,
            self.trade_buy_class,
        )

        self.strategy_sell = self.build_strategy_sell(
            self.filter_sell_class,
            self.trigger_sell_class,
            self.trade_sell_class,
        )

        # Define other strategy components
        self.trend_class = db.get_class_code("UpTrend_Price_gt_SMAlong")
        self.trend_analysis = self.build_trend_analysis(self.trend_class)
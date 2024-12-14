from common.python.strategybuy import StrategyBuy
from common.python.strategysell import StrategySell
from common.python.trendanalysis import TrendAnalysis

class StrategyLong:
    """
    Base class for LONG strategies, encapsulating the logic for buying and selling.
    Subclasses must define the necessary attributes, such as `trend_analysis`,
    and provide the components for `strategy_buy` and `strategy_sell` construction.
    """

    def __init__(self):
        # Attributes to be defined by subclasses
        self.strategy_buy = None
        self.strategy_sell = None
        self.trend_analysis = None

    def ShouldBuy(self):
        if self.trend_analysis.is_upTrend():
            return self.strategy_buy.shouldBuy()
        return False

    def ShouldSell(self):
        return self.strategy_sell.shouldSell()


    def build_strategy_buy(self, filter_class, trigger_class, trade_class):
        """
        Constructs the strategy buy logic using the provided classes.
        """
        return StrategyBuy(
            filter_class=filter_class,
            trigger_class=trigger_class,
            trade_class=trade_class,
        )

    def build_strategy_sell(self, filter_class, trigger_class, trade_class):
        """
        Constructs the strategy sell logic using the provided classes.
        """
        return StrategySell(
            filter_class=filter_class,
            trigger_class=trigger_class,
            trade_class=trade_class,
        )
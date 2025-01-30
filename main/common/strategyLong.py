from common.strategybuy import StrategyBuy
from common.strategysell import StrategySell
from common.trendanalysis import TrendAnalysis

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

    def ShouldOpen(self):
        if self.trend_analysis.is_upTrend():
            return self.strategy_buy.shouldBuy()
        return False

    def ShouldClose(self):
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

    def build_trend_analysis(self, trend_class):
        """
        Constructs the trend analysis logic using the provided class and parameters.
        """
        return TrendAnalysis(
            trend_class=trend_class
        )
    
    def get_biggest_trend_interval(self):
        """
        Finds the largest value among all attributes that start with 'trend'.

        Returns:
            int: The largest value among 'trend' attributes.
        """

        # array with all values related to trend indicators.
        trend_values = [
            # vars(self): gets a dict with all attributes of the class.
            # the loop below iterates all keys (name) and values of those attributes.
            # isinstance: checks if the attribute value is an int or float.
            value for name, value in vars(self).items()
            if name.startswith("trend") and isinstance(value, (int, float))
        ]

        if not trend_values:
            raise ValueError("No 'trend' attributes defined in this strategy.")
        return max(trend_values)
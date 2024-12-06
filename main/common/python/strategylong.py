from common.python.strategybuy import StrategyBuy
from common.python.strategysell import StrategySell
from common.python.trendanalysis import TrendAnalysis

class StrategyLong():
    def __init__(self, dataset):
        self.dataset = dataset
        self.strategyBuy = StrategyBuy()
        self.strategySell = StrategySell()
        self.trendAnalysis = TrendAnalysis()

    def shouldBuy(self):
        return self.strategyBuy.shouldBuy() if self.trendAnalysis.is_upTrend() else False

    def shouldSell(self):
        return self.strategySell.shouldSell()
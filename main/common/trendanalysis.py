class TrendAnalysis():
    def __init__(self, trend_class):
        self.trend = trend_class

    def is_onTrend(self):
        return self.trend.ontrend()
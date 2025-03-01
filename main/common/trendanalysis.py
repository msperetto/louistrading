class TrendAnalysis():
    def __init__(self, trend):
        self.trend = trend

    def is_onTrend(self):
        return self.trend.ontrend()
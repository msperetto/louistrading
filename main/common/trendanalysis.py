class TrendAnalysis():
    def __init__(self, trend):
        self.trend = trend

    def is_upTrend(self):
        if self.trend.__class__.__name__[0:self.trend.__class__.__name__.find("_")] == "UpTrend":
            return self.trend.ontrend()

    def is_downTrend(self):
        if self.trend.__class__.__name__[0:self.trend.__class__.__name__.find("_")] == "DownTrend":
            return self.trend.ontrend()


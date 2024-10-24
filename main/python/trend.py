from abc import ABC


class Trend(ABC):
    def ontrend(self):
        pass

class UpTrend_EMAshort_gt_SMAlong(Trend):
    def __init__(self, ema_short_fn, sma_long_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def ontrend(self):
        return self.get_ema_short()[-1] > self.get_sma_long()[-1]


class AlwaysTrend(Trend):
    def ontrend(self):
        return True

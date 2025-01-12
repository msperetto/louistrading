from abc import ABC
from common import util

class Trend(ABC):
    def ontrend(self):
        pass

class UpTrend_EMAshort_gt_SMAlong(Trend):
    def __init__(self, ema_short_fn, sma_long_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def ontrend(self):
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1)

class UpTrend_EMAshort_gt_SMAmedium(Trend):
    def __init__(self, ema_short_fn, sma_medium_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def ontrend(self):
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1)

class UpTrend_SMAmedium_gt_SMAlong(Trend):
    def __init__(self, sma_medium_fn, sma_long_fn):
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def ontrend(self):
        return  util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1)


class UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong(Trend):
    def __init__(self, ema_short_fn,sma_medium_fn, sma_long_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def ontrend(self):
        return (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1)) \
                and (util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1))


class UpTrend_Price_gt_SMAmedium(Trend):
    def __init__(self, data, sma_medium_fn):
        self.data = data
        self.get_sma_medium = sma_medium_fn

    def ontrend(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_medium(), -1)


class UpTrend_Price_gt_SMAlong(Trend):
    def __init__(self, data, sma_long_fn):
        self.data = data
        self.get_sma_long = sma_long_fn

    def ontrend(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_long(), -1)

class UpTrend_Price_gt_EMAshort(Trend):
    def __init__(self, data, ema_short_fn):
        self.data = data
        self.get_ema_short = ema_short_fn

    def ontrend(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_ema_short(), -1)


class UpTrend_EMAshort_gt_SMAlong_ADX(Trend):
    def __init__(self, ema_short_fn, sma_long_fn, adx_fn, adx_trend_layer):
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn
        self.get_adx = adx_fn
        self.adx_trend_layer = adx_trend_layer

    def ontrend(self):
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1) and \
               util.get_value_by_index(self.get_adx(), -1) > self.adx_trend_layer

class UpTrend_EMAshort_gt_SMAmedium_ADX(Trend):
    def __init__(self, ema_short_fn, sma_medium_fn, adx_fn, adx_trend_layer):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_adx = adx_fn
        self.adx_trend_layer = adx_trend_layer

    def ontrend(self):
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1) and \
               util.get_value_by_index(self.get_adx(), -1) > self.adx_trend_layer


class UpTrend_SMAmedium_gt_SMAlong_ADX(Trend):
    def __init__(self, sma_medium_fn, sma_long_fn, adx_fn, adx_trend_layer):
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn
        self.get_adx = adx_fn
        self.adx_trend_layer = adx_trend_layer

    def ontrend(self):
        return util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1) and \
        util.get_value_by_index(self.get_adx(), -1) > self.adx_trend_layer

class UpTrend_AlwaysTrend(Trend):
    def ontrend(self):
        return True

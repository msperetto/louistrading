from abc import ABC
from common import util

class Filter(ABC):
    def isValid(self) -> bool:
        pass

class Filter_alwaysTrue(Filter):
    def isValid(self) -> bool:
        return True


class FilterBuy_RSI(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap

    def isValid(self) -> bool:
        return util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap

class FilterBuy_RSI_EMAshort_gt_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, ema_short_fn, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_EMAshort_gt_SMAlong(Filter):
    def __init__(self, ema_short_fn, sma_long_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1)

class FilterBuy_EMAshort_gt_SMAmedium(Filter):
    def __init__(self, ema_short_fn, sma_medium_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def isValid(self) -> bool:
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1)

class FilterBuy_RSI_EMAshort_gt_SMAmedium(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, ema_short_fn, sma_medium_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, ema_short_fn, sma_medium_fn, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1)) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, ema_short_fn, sma_medium_fn, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1)) and \
               (util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong(Filter):
    def __init__(self, ema_short_fn, sma_medium_fn, sma_long_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_ema_short(), -1) < util.get_value_by_index(self.get_sma_medium(), -1)) and \
               (util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium(Filter):
    def __init__(self, ema_short_fn, sma_medium_fn, sma_long_fn, data):
        self.data = data
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_ema_short(), -1) < util.get_value_by_index(self.get_sma_medium(), -1)) and \
               (util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1)) and \
               (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_medium(), -1))

class FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong(Filter):
    def __init__(self, ema_short_fn, sma_medium_fn, sma_long_fn, data):
        self.data = data
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_ema_short(), -1) < util.get_value_by_index(self.get_sma_medium(), -1)) and \
               (util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1)) and \
               (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_RSI_price_x_SMAmedium(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, data, sma_medium_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.data = data
        self.get_sma_medium = sma_medium_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_medium(), -1))

class FilterBuy_RSI_price_x_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, data, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.data = data
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, data, sma_medium_fn, ema_short_fn, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.data = data
        self.get_sma_medium = sma_medium_fn
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1)) and \
               (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_medium(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, data, sma_long_fn, ema_short_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.data = data
        self.get_sma_long = sma_long_fn
        self.get_ema_short = ema_short_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_rsi(), -1) < self.rsi_layer_cheap) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_long(), -1)) and \
               (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_long(), -1))

class FilterBuy_SMAmedium_gt_SMAlong(Filter):
    def __init__(self, sma_medium_fn, sma_long_fn):
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1)

class FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium(Filter):
    def __init__(self, data, sma_medium_fn, sma_long_fn):
        self.data = data
        self.get_sma_medium = sma_medium_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.get_sma_medium(), -1) > util.get_value_by_index(self.get_sma_long(), -1)) or \
               ((util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_long(), -1)) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_medium(), -1)))

class FilterSell_RSI(Filter):
    def __init__(self, rsi_fn, rsi_layer_expensive):
        self.get_rsi = rsi_fn
        self.rsi_layer_expensive = rsi_layer_expensive

    def isValid(self) -> bool:
        return util.get_value_by_index(self.get_rsi(), -1) > self.rsi_layer_expensive
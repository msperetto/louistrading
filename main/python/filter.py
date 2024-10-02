from abc import ABC
import inspect

class Filter(ABC):
    def isValid(self) -> bool:
        pass


class Filter_alwaysTrue(Filter):
    def isValid(self) -> bool:
        return True


class FilterBuy_RSI(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap):
        # print(rsi_fn())
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap

    def isValid(self) -> bool:
        return self.get_rsi()[-1] < self.rsi_layer_cheap

class FilterBuy_RSI_EMAshort_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, ema_short_fn, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (self.get_rsi()[-1] < self.rsi_layer_cheap) and (self.get_ema_short()[-1] > self.get_sma_long()[-1])

class FilterBuy_RSI_price_x_SMAlong(Filter):
    def __init__(self, rsi_fn, rsi_layer_cheap, data, sma_long_fn):
        self.get_rsi = rsi_fn
        self.rsi_layer_cheap = rsi_layer_cheap
        self.data = data
        self.get_sma_long = sma_long_fn

    def isValid(self) -> bool:
        return (self.get_rsi()[-1] < self.rsi_layer_cheap) and (self.data.Close[-1] > self.get_sma_long()[-1])


class FilterSell_RSI(Filter):
    def __init__(self, rsi_fn, rsi_layer_expensive):
        self.get_rsi = rsi_fn
        self.rsi_layer_expensive = rsi_layer_expensive

    def isValid(self) -> bool:
        if (self.get_rsi()[-1] > self.rsi_layer_expensive):
            return True
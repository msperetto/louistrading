from abc import ABC

class Filter(ABC):
    def isValid(self) -> bool:
        pass


class FilterBuy_RSI(Filter):
    def __init__(self, rsi, rsi_layer_cheap):
        self.rsi = rsi
        self.rsi_layer_cheap = rsi_layer_cheap

    def isValid(self) -> bool:
        if (self.rsi < self.rsi_layer_cheap):
            return True
        return False


class FilterBuy_RSI_SMA(Filter):
    def __init__(self, rsi, rsi_layer_cheap, sma1, sma2):
        self.rsi = rsi
        self.rsi_layer_cheap = rsi_layer_cheap
        self.sma1 = sma1
        self.sma2 = sma2

    def isValid(self) -> bool:
        if (self.rsi < self.rsi_layer_cheap) and (self.sma1 > self.sma2):
            return True
        return False


class FilterSell_RSI(Filter):
    def __init__(self, rsi, rsi_layer_expensive):
        self.rsi = rsi
        self.rsi_layer_expensive = rsi_layer_expensive

    def isValid(self) -> bool:
        if (self.rsi > self.rsi_layer_expensive):
            return True
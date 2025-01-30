from abc import ABC
from common import util


class Trade(ABC):
    def buyConfirmation(self):
        pass

    def sellConfirmation(self):
        pass


class TradeBuy_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.High, -2)

class TradeBuy_Price_gt_EMAshort(Trade):
    def __init__(self, data, ema_short_fn):
        self.data = data
        self.get_ema_short = ema_short_fn

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_ema_short(), -1)

class TradeBuy_Price_gt_SMAmedium(Trade):
    def __init__(self, data, sma_medium_fn):
        self.data = data
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.get_sma_medium(), -1)

class TradeBuy_EMAshort_gt_SMAmedium(Trade):
    def __init__(self, ema_short_fn, sma_medium_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1)

class TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(Trade):
    def __init__(self, ema_short_fn, sma_medium_fn, data):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1) and \
               util.get_value_by_index(self.data.High, -1) > util.get_value_by_index(self.data.High, -2)

class TradeBuy_Close_gt_CloseLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.Close, -2)

class TradeBuy_High_x_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.High, -1) > util.get_value_by_index(self.data.High, -2)

class TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium(Trade):
    def __init__(self, data, ema_short_fn, sma_medium_fn):
        self.data = data
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.High, -2)) and \
               (util.get_value_by_index(self.get_ema_short(), -1) > util.get_value_by_index(self.get_sma_medium(), -1))

class TradeSell_LowLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.data.Low, -2)

class TradeSell_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.data.High, -2)

class TradeSell_Price_EMAshort(Trade):
    def __init__(self, data, fn_ema_short):
        self.data = data
        self.get_ema_p_short = fn_ema_short

    def sellConfirmation(self) -> bool:
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.get_ema_p_short(), -1)
from abc import ABC
from common import util
from common.factory import Factory

class Trade(ABC):
    def buyConfirmation(self):
        pass

    def sellConfirmation(self):
        pass

    # Factory method to create and instantiate a Trade object
    def trade_factory(self, class_name: str, obj_caller, **kwargs):
        return Factory.create(class_name, obj_caller, **kwargs)

class TradeBuy_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.High, -2)

class TradeBuy_Price_gt_EMAshort(Trade):
    def __init__(self, data, intraday_ema_short):
        self.data = data
        self.intraday_ema_short = intraday_ema_short

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_ema_short(), -1)

class TradeBuy_Price_gt_SMAmedium(Trade):
    def __init__(self, data, intraday_sma_medium):
        self.data = data
        self.intraday_sma_medium = intraday_sma_medium

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_medium(), -1)

class TradeBuy_EMAshort_gt_SMAmedium(Trade):
    def __init__(self, intraday_ema_short, intraday_sma_medium):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def buyConfirmation(self):
        return util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1)

class TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(Trade):
    def __init__(self, intraday_ema_short, intraday_sma_medium, data):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1) and \
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
    def __init__(self, data, intraday_ema_short, intraday_sma_medium):
        self.data = data
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def buyConfirmation(self):
        return (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.High, -2)) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1))
    
class TradeBuy_Close_gt_CloseLastCandle_EMAshort_gt_SMAmedium(Trade):
    def __init__(self, data, intraday_ema_short, intraday_sma_medium):
        self.data = data
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def buyConfirmation(self):
        return (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.Close, -2)) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1))

class TradeBuy_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.data.High, -2)
    
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

class TradeSell_Price_lt_EMAshort(Trade):
    def __init__(self, data, intraday_ema_short):
        self.data = data
        self.intraday_ema_short = intraday_ema_short

    def sellConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.intraday_ema_short(), -1)

class TradeSell_Price_lt_SMAmedium(Trade):
    def __init__(self, data, intraday_sma_medium):
        self.data = data
        self.intraday_sma_medium = intraday_sma_medium

    def sellConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.intraday_sma_medium(), -1)

class TradeSell_EMAshort_lt_SMAmedium(Trade):
    def __init__(self, intraday_ema_short, intraday_sma_medium):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def sellConfirmation(self):
        return util.get_value_by_index(self.intraday_ema_short(), -1) < util.get_value_by_index(self.intraday_sma_medium(), -1)

class TradeSell_EMAshort_lt_SMAmedium_Low_lt_LowLastCandle(Trade):
    def __init__(self, intraday_ema_short, intraday_sma_medium, data):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.data = data

    def sellConfirmation(self):
        return util.get_value_by_index(self.intraday_ema_short(), -1) < util.get_value_by_index(self.intraday_sma_medium(), -1) and \
                util.get_value_by_index(self.data.Low, -1) < util.get_value_by_index(self.data.Low, -2)

class TradeSell_LowLastCandle_EMAshort_lt_SMAmedium(Trade):
    def __init__(self, data, intraday_ema_short, intraday_sma_medium):
        self.data = data
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def sellConfirmation(self):
        return (util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.data.High, -2)) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) < util.get_value_by_index(self.intraday_sma_medium(), -1))

class TradeSell_Low_lt_LowLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        return util.get_value_by_index(self.data.Low, -1) < util.get_value_by_index(self.data.Low, -2)

class TradeSell_EMAshort_lt_SMAmedium_High_lt_HighLastCandle(Trade):
    def __init__(self, intraday_ema_short, intraday_sma_medium, data):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.data = data

    def sellConfirmation(self):
        return util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1) and \
                util.get_value_by_index(self.data.High, -1) > util.get_value_by_index(self.data.High, -2)

class TradeSell_Close_lt_CloseLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.data.Close, -2)
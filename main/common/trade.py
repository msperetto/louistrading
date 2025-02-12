from abc import ABC
from common import util
from backtesting._util import _Indicator


class Trade(ABC):
    def buyConfirmation(self):
        pass

    def sellConfirmation(self):
        pass

    # Factory method to create and instantiate a Trade object
    def trade_factory(self, class_name: str, obj_caller, **kwargs) -> 'Trade':
        # Get the class from the global namespace
        cls = globals().get(class_name)
        if not cls:
            raise ValueError(f"Class {class_name} not found")
    
        # Get the constructor parameters for the class of class_name
        constructor_params = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]
    
        # Filter the kwargs to include only the parameters needed by the constructor
        filtered_kwargs = {key: kwargs[key] for key in constructor_params if key in kwargs}

        # Convert the parameters to lambda functions if they are _Indicator (a list) and not 'data'
        lambda_kwargs = {key: (lambda self=self, key=key: getattr(obj_caller, key)[:len(getattr(obj_caller, key))]) if isinstance(value, _Indicator) and key != 'data' else value for key, value in filtered_kwargs.items()}

        # Instantiate the class with the lambda parameters
        return cls(**lambda_kwargs)

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
    def __init__(self, data, intraday_ema_short):
        self.data = data
        self.intraday_ema_short = intraday_ema_short

    def sellConfirmation(self) -> bool:
        return util.get_value_by_index(self.data.Close, -1) < util.get_value_by_index(self.intraday_ema_short(), -1)
from abc import ABC
from common import util
from backtesting._util import _Indicator

class Filter(ABC):
    def isValid(self) -> bool:
        pass

    # Factory method to create and instantiate a Filter object
    def filter_factory(self, class_name: str, obj_caller, **kwargs) -> 'Filter':
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

class Filter_alwaysTrue(Filter):
    def __init__(self):
        pass

    def isValid(self) -> bool:
        return True

class FilterBuy_RSI(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap

    def isValid(self) -> bool:
        return util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap


class FilterBuy_RSI_EMAshort_gt_SMAlong(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, intraday_ema_short, intraday_sma_long):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_EMAshort_gt_SMAlong(Filter):
    def __init__(self, intraday_ema_short, intraday_sma_long):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)

class FilterBuy_EMAshort_gt_SMAmedium(Filter):
    def __init__(self, intraday_ema_short, intraday_sma_medium):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def isValid(self) -> bool:
        return util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1)

class FilterBuy_RSI_EMAshort_gt_SMAmedium(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, intraday_ema_short, intraday_sma_medium):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, intraday_ema_short, intraday_sma_medium, intraday_sma_long):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1)) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, intraday_ema_short, intraday_sma_medium, intraday_sma_long):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_medium(), -1)) and \
                (util.get_value_by_index(self.intraday_sma_medium(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong(Filter):
    def __init__(self, intraday_ema_short, intraday_sma_medium, intraday_sma_long):
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_ema_short(), -1) < util.get_value_by_index(self.intraday_sma_medium(), -1)) and \
                (util.get_value_by_index(self.intraday_sma_medium(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium(Filter):
    def __init__(self, intraday_ema_short, intraday_sma_medium, intraday_sma_long, data):
        self.data = data
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_ema_short(), -1) < util.get_value_by_index(self.intraday_sma_medium(), -1)) and \
                (util.get_value_by_index(self.intraday_sma_medium(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_medium(), -1))

class FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong(Filter):
    def __init__(self, intraday_ema_short, intraday_sma_medium, intraday_sma_long, data):
        self.data = data
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_ema_short(), -1) < util.get_value_by_index(self.intraday_sma_medium(), -1)) and \
                (util.get_value_by_index(self.intraday_sma_medium(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_RSI_price_x_SMAmedium(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, data, intraday_sma_medium):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.data = data
        self.intraday_sma_medium = intraday_sma_medium

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_medium(), -1))

class FilterBuy_RSI_price_x_SMAlong(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, data, intraday_sma_long):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.data = data
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, data, intraday_sma_medium, intraday_ema_short, intraday_sma_long):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.data = data
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_ema_short = intraday_ema_short
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_medium(), -1))

class FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_cheap, data, intraday_sma_long, intraday_ema_short):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_cheap = intraday_rsi_layer_cheap
        self.data = data
        self.intraday_sma_long = intraday_sma_long
        self.intraday_ema_short = intraday_ema_short

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_rsi(), -1) < self.intraday_rsi_layer_cheap) and \
                (util.get_value_by_index(self.intraday_ema_short(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_long(), -1))

class FilterBuy_SMAmedium_gt_SMAlong(Filter):
    def __init__(self, intraday_sma_medium, intraday_sma_long):
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return util.get_value_by_index(self.intraday_sma_medium(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)

class FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium(Filter):
    def __init__(self, data, intraday_sma_medium, intraday_sma_long):
        self.data = data
        self.intraday_sma_medium = intraday_sma_medium
        self.intraday_sma_long = intraday_sma_long

    def isValid(self) -> bool:
        return (util.get_value_by_index(self.intraday_sma_medium(), -1) > util.get_value_by_index(self.intraday_sma_long(), -1)) or \
                ((util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_long(), -1)) and \
                (util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.intraday_sma_medium(), -1)))

class FilterSell_RSI(Filter):
    def __init__(self, intraday_rsi, intraday_rsi_layer_expensive):
        self.intraday_rsi = intraday_rsi
        self.intraday_rsi_layer_expensive = intraday_rsi_layer_expensive

    def isValid(self) -> bool:
        return util.get_value_by_index(self.intraday_rsi(), -1) > self.intraday_rsi_layer_expensive

from abc import ABC
from common import util

class Trend(ABC):
    def ontrend(self):
        pass

    # Factory method to create and instantiate a Trend object
    def trend_factory(self, class_name: str, **kwargs) -> 'Trend':
        # Get the class from the global namespace
        cls = globals().get(class_name)
        if not cls:
            raise ValueError(f"Class {class_name} not found")
    
        # Get the constructor parameters for the class of class_name
        constructor_params = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]
    
        # Filter the kwargs to include only the parameters needed by the constructor
        filtered_kwargs = {key: kwargs[key] for key in constructor_params if key in kwargs}
    
        # Instantiate the class with the filtered parameters
        return cls(**filtered_kwargs)
        
class UpTrend_EMAshort_gt_SMAlong(Trend):
    def __init__(self, trend_ema_short, trend_sma_long):
        self.trend_ema_short = trend_ema_short
        self.trend_sma_long = trend_sma_long

    def ontrend(self):
        return util.get_value_by_index(self.trend_ema_short, -1) > util.get_value_by_index(self.trend_sma_long, -1)

class UpTrend_EMAshort_gt_SMAmedium(Trend):
    def __init__(self, trend_ema_short, trend_sma_medium):
        self.trend_ema_short = trend_ema_short
        self.trend_sma_medium = trend_sma_medium

    def ontrend(self):
        return util.get_value_by_index(self.trend_ema_short, -1) > util.get_value_by_index(self.trend_sma_medium, -1)

class UpTrend_SMAmedium_gt_SMAlong(Trend):
    def __init__(self, trend_sma_medium, trend_sma_long):
        self.trend_sma_medium = trend_sma_medium
        self.trend_sma_long = trend_sma_long

    def ontrend(self):
        return util.get_value_by_index(self.trend_sma_medium, -1) > util.get_value_by_index(self.trend_sma_long, -1)

class UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong(Trend):
    def __init__(self, trend_ema_short, trend_sma_medium, trend_sma_long):
        self.trend_ema_short = trend_ema_short
        self.trend_sma_medium = trend_sma_medium
        self.trend_sma_long = trend_sma_long

    def ontrend(self):
        return (util.get_value_by_index(self.trend_ema_short, -1) > util.get_value_by_index(self.trend_sma_medium, -1)) \
                and (util.get_value_by_index(self.trend_sma_medium, -1) > util.get_value_by_index(self.trend_sma_long, -1))

class UpTrend_Price_gt_SMAmedium(Trend):
    def __init__(self, data, trend_sma_medium):
        self.data = data
        self.trend_sma_medium = trend_sma_medium

    def ontrend(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.trend_sma_medium, -1)

class UpTrend_Price_gt_SMAlong(Trend):
    def __init__(self, data, trend_sma_long):
        self.data = data
        self.trend_sma_long = trend_sma_long

    def ontrend(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.trend_sma_long, -1)

class UpTrend_Price_gt_EMAshort(Trend):
    def __init__(self, data, trend_ema_short):
        self.data = data
        self.trend_ema_short = trend_ema_short

    def ontrend(self):
        return util.get_value_by_index(self.data.Close, -1) > util.get_value_by_index(self.trend_ema_short, -1)

class UpTrend_EMAshort_gt_SMAlong_ADX(Trend):
    def __init__(self, trend_ema_short, trend_sma_long, trend_adx, trend_adx_trend_layer):
        self.trend_ema_short = trend_ema_short
        self.trend_sma_long = trend_sma_long
        self.trend_adx = trend_adx
        self.trend_adx_trend_layer = trend_adx_trend_layer

    def ontrend(self):
        return util.get_value_by_index(self.trend_ema_short, -1) > util.get_value_by_index(self.trend_sma_long, -1) and \
                util.get_value_by_index(self.trend_adx, -1) > self.trend_adx_trend_layer

class UpTrend_EMAshort_gt_SMAmedium_ADX(Trend):
    def __init__(self, trend_ema_short, trend_sma_medium, trend_adx, trend_adx_trend_layer):
        self.trend_ema_short = trend_ema_short
        self.trend_sma_medium = trend_sma_medium
        self.trend_adx = trend_adx
        self.trend_adx_trend_layer = trend_adx_trend_layer

    def ontrend(self):
        return util.get_value_by_index(self.trend_ema_short, -1) > util.get_value_by_index(self.trend_sma_medium, -1) and \
                util.get_value_by_index(self.trend_adx, -1) > self.trend_adx_trend_layer

class UpTrend_SMAmedium_gt_SMAlong_ADX(Trend):
    def __init__(self, trend_sma_medium, trend_sma_long, trend_adx, trend_adx_trend_layer):
        self.trend_sma_medium = trend_sma_medium
        self.trend_sma_long = trend_sma_long
        self.trend_adx = trend_adx
        self.trend_adx_trend_layer = trend_adx_trend_layer

    def ontrend(self):
        return util.get_value_by_index(self.trend_sma_medium, -1) > util.get_value_by_index(self.trend_sma_long, -1) and \
                util.get_value_by_index(self.trend_adx, -1) > self.trend_adx_trend_layer

class UpTrend_AlwaysTrend(Trend):
    def __init__(self):
        pass
    
    def ontrend(self):
        return True

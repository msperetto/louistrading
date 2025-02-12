from abc import ABC
from backtesting._util import _Indicator

class TriggeredState(ABC):
    def isStillValid(self) -> bool:
        pass

    def reset(self):
        pass

    # Factory method to create and instantiate a Filter object
    def trigger_factory(self, class_name: str, obj_caller, **kwargs) -> 'Trigger':
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

# 
class TriggeredState_alwaysTrue(TriggeredState):
    def __init__(self):
        self.is_filtered = False

    def reset(self, is_filtered):
        self.is_filtered = is_filtered

    def isStillValid(self) -> bool:
        return self.is_filtered


class TriggeredState_MaxCandles_Buy(TriggeredState):
    def __init__(self, intraday_max_candles_buy):
        self.intraday_max_candles = intraday_max_candles_buy
        self.intraday_candles_after_triggered = intraday_max_candles_buy

    def reset(self, intraday_is_filtered):
        if intraday_is_filtered:
            self.intraday_candles_after_triggered = 0

    def isStillValid(self):
        if self.intraday_candles_after_triggered < self.intraday_max_candles:
            self.intraday_candles_after_triggered += 1
            return True
        elif self.intraday_candles_after_triggered >= self.intraday_max_candles:
            return False


class TriggeredState_MaxCandles_Sell(TriggeredState):
    def __init__(self, intraday_max_candles_sell):
        self.intraday_max_candles = intraday_max_candles_sell
        self.intraday_candles_after_triggered = intraday_max_candles_sell

    def reset(self, intraday_is_filtered):
        if intraday_is_filtered:
            self.intraday_candles_after_triggered = 0

    def isStillValid(self):
        if self.intraday_candles_after_triggered < self.intraday_max_candles:
            self.intraday_candles_after_triggered += 1
            return True
        elif self.intraday_candles_after_triggered >= self.intraday_max_candles:
            return False


class TriggeredState_MaxCandles_EMAshort_SMAlong_Price_SMAlong(TriggeredState):
    def __init__(self, intraday_max_candles, intraday_ema_short, intraday_sma_long, data):
        self.intraday_max_candles = intraday_max_candles
        self.intraday_candles_after_triggered = intraday_max_candles
        self.data = data
        self.ema_short = intraday_ema_short
        self.sma_long = intraday_sma_long

    def reset(self, intraday_is_filtered):
        if intraday_is_filtered:
            self.intraday_candles_after_triggered = 0

    def isStillValid(self):
        if self.intraday_candles_after_triggered < self.intraday_max_candles:
            self.intraday_candles_after_triggered += 1
            return True
        elif self.intraday_candles_after_triggered >= self.intraday_max_candles:
            return False


class TriggeredState_MaxCandles_LongSma(TriggeredState):
    def reset(self):
        pass

    def isStillValid(self):
        pass

from abc import ABC

class TriggeredState(ABC):
    def isStillValid(self) -> bool:
        pass

    def reset(self):
        pass

# 
class TriggeredState_alwaysTrue(TriggeredState):
    def __init__(self):
        self.is_filtered = False

    def reset(self, is_filtered):
        self.is_filtered = is_filtered

    def isStillValid(self) -> bool:
        return self.is_filtered


class TriggeredState_MaxCandles(TriggeredState):
    def __init__(self, max_candles):
        self.max_candles = max_candles
        self.candles_after_triggered = max_candles
        # self.triggered = False

    def reset(self, is_filtered):
        if is_filtered:
            self.candles_after_triggered = 0

    def isStillValid(self):
        # starting to count the next candles after triggered
        # if self.triggered and self.candles_after_triggered < self.max_candles:
        if self.candles_after_triggered < self.max_candles:
            self.candles_after_triggered += 1
            return True
        
        # untriggering after max_candles
        elif self.candles_after_triggered >= self.max_candles:
            # self.candles_after_triggered = 0
            # self.triggered = False 
            return False


#not finished, but not sure if is needed
class TriggeredState_MaxCandles_EMAshort_SMAlong_Price_SMAlong(TriggeredState):
    def __init__(self, max_candles, ema_short_fn, sma_long_fn, data):
        self.max_candles = max_candles
        self.candles_after_triggered = max_candles
        self.data = data
        self.get_ema_short = ema_short_fn
        self.get_sma_long = sma_long_fn

    def reset(self, is_filtered):
        if is_filtered:
            self.candles_after_triggered = 0

    def isStillValid(self):
        # starting to count the next candles after triggered
        # if self.triggered and self.candles_after_triggered < self.max_candles:
        if self.candles_after_triggered < self.max_candles:
            self.candles_after_triggered += 1
            return True
        
        # untriggering after max_candles
        elif self.candles_after_triggered >= self.max_candles:
            # self.candles_after_triggered = 0
            # self.triggered = False 
            return False


class TriggeredState_MaxCandles_LongSma(TriggeredState):
    def reset(self):
        pass

    def isStillValid(self):
        pass
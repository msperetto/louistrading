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
    def __init__(self, intraday_max_candles):
        self.intraday_max_candles = intraday_max_candles
        self.intraday_candles_after_triggered = intraday_max_candles

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

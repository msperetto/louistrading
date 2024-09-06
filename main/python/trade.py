from abc import ABC


class Trade(ABC):
    def buyConfirmation(self):
        pass

    def sellConfirmation(self):
        pass


class Trade_Buy_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        if self.data.Close[-1] > self.data.High[-2]:
            return True


class Trade_Buy_HighLastCandle_EMA_short_SMA_medium(Trade):
    def __init__(self, data, ema_short_fn, sma_medium_fn):
        self.data = data
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return (self.data.Close[-1] > self.data.High[-2]) and (self.get_ema_short()[-1] > self.get_sma_medium()[-1])


class Trade_Sell_LowLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        if self.data.Close[-1] < self.data.Low[-2]:
            return True

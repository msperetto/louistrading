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


class Trade_Sell_LowLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        if self.data.Close[-1] < self.data.Low[-2]:
            return True

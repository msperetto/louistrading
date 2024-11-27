from abc import ABC


class Trade(ABC):
    def buyConfirmation(self):
        pass

    def sellConfirmation(self):
        pass


class TradeBuy_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return self.data.Close[-1] > self.data.High[-2]

class TradeBuy_Price_gt_EMAshort(Trade):
    def __init__(self, data, ema_short_fn):
        self.data = data
        self.get_ema_short = ema_short_fn

    def buyConfirmation(self):
        return self.data.Close[-1] > self.get_ema_short()[-1]

class TradeBuy_Price_gt_SMAmedium(Trade):
    def __init__(self, data, sma_medium_fn):
        self.data = data
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return self.data.Close[-1] > self.get_sma_medium()[-1]

class TradeBuy_EMAshort_gt_SMAmedium(Trade):
    def __init__(self, ema_short_fn, sma_medium_fn):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return self.get_ema_short()[-1] > self.get_sma_medium()[-1]

class TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(Trade):
    def __init__(self, ema_short_fn, sma_medium_fn, data):
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn
        self.data = data

    def buyConfirmation(self):
        return self.get_ema_short()[-1] > self.get_sma_medium()[-1] and \
                self.data.High[-1] > self.data.High[-2]

class TradeBuy_Close_gt_CloseLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return self.data.Close[-1] > self.data.Close[-2]
 
class TradeBuy_High_x_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def buyConfirmation(self):
        return self.data.High[-1] > self.data.High[-2]

class TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium(Trade):
    def __init__(self, data, ema_short_fn, sma_medium_fn):
        self.data = data
        self.get_ema_short = ema_short_fn
        self.get_sma_medium = sma_medium_fn

    def buyConfirmation(self):
        return (self.data.Close[-1] > self.data.High[-2]) and (self.get_ema_short()[-1] > self.get_sma_medium()[-1])


class TradeSell_LowLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        return self.data.Close[-1] < self.data.Low[-2]

class TradeSell_HighLastCandle(Trade):
    def __init__(self, data):
        self.data = data

    def sellConfirmation(self):
        if self.data.Close[-1] < self.data.High[-2]:
            return True

class TradeSell_Price_EMAshort(Trade):
    def __init__(self, data, fn_ema_short):
        self.data = data
        self.get_ema_p_short = fn_ema_short

    def sellConfirmation(self) -> bool:
        return self.data.Close[-1] < self.get_ema_p_short()[-1]

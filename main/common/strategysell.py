class StrategySell():
    def __init__(self, filter_class, trigger_class, trade_class):
        self.filter = filter_class
        self.triggeredState = trigger_class
        self.trade = trade_class

    def shouldSell(self):
        if self.filter.isValid():
            self.triggeredState.reset(True)
        else: self.triggeredState.reset(False)

        if self.triggeredState.isStillValid():
            if self.trade.sellConfirmation(): return True
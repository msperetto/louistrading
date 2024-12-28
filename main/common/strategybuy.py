class StrategyBuy():
    def __init__(self, filterBuy, triggeredState, trade):
        self.filter = filterBuy
        self.triggeredState = triggeredState
        self.trade = trade

    def shouldBuy(self):
        if self.filter.isValid(): 
            self.triggeredState.reset(True)
        else: self.triggeredState.reset(False)

        if self.triggeredState.isStillValid():
            if self.trade.buyConfirmation(): return True
 
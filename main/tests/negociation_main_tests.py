import pandas as pd

class TestNegociationMain():
    test_fake_candle = {
        'Open': 105000,
        'High': 110000,
        'Low': 100000,
        'Close': 107900,
        'Volume': 4000,
        'EMA_8': 108900,
        'EMA_9': 108000,
        'SMA_19': 108500,
        'SMA_20': 108500,
        'SMA_49': 109000,
        'SMA_51': 109000,
        'TREND_SMA_19': 109000,
        'TREND_SMA_50': 109000
    }
    new_fake_index = pd.Timestamp('2025-03-14 12:00:00')
    new_fake_row = pd.DataFrame([test_fake_candle], index=[new_fake_index])

    def add_fake_row(self, df):
        return pd.concat([df, self.new_fake_row])


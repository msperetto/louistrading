import pandas as pd

class TestNegociationMain():
    test_fake_candle = {
        'Open': 105000,
        'High': 110000,
        'Low': 100000,
        'Close': 108900,
        'Volume': 4000,
        'EMA_8': 108000,
        'SMA_44': 107000,
        'TREND_SMA_7': 103000
    }
    new_fake_index = pd.Timestamp('2024-12-18 14:00:00')
    new_fake_row = pd.DataFrame([test_fake_candle], index=[new_fake_index])

    def add_fake_row(self, df):
        return pd.concat([df, self.new_fake_row])


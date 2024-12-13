import pandas as pd
from prod.python.binance import Binance as binance
from common.python import database_operations as db

class Ohcl():
    def __init__(self, pair, interval, startTime):
        self.pair = pair
        self.interval = interval
        self.startTime = startTime
    
    def populate_ohlc(self):
        self.ohcl_df = binance().get_extended_kline(self.pair, self.interval, self.startTime)

    def get_new_row(self):
        # get 2 last candles provided and uses the second one (the first one is the current changing candle)
        return binance().get_kline(self.pair, self.interval, None, None, 2).iloc[0]

    def append_row_to_df(self, row):
        self.ohcl_df.loc[len(self.ohcl_df)] = row

    def update_dataset(self, row):
        self.append_row_to_df(row)
        self.ohcl_df.drop([0])

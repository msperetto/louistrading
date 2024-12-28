import pandas as pd
from prod.python.binance import Binance as binance
from common.python import database_operations as db

class CandleData():
    def __init__(self, pair, interval, startTime):
        self.pair = pair
        self.interval = interval
        self.startTime = startTime
    
    def populate_data(self, endTime):
        self.candle_df = binance().get_extended_kline(self.pair, self.interval, self.startTime, endTime)

    def get_new_row(self):
        # get 2 last candles provided and uses the second one (the first one is the current changing candle)
        return binance().get_kline(self.pair, self.interval, None, None, 2).iloc[0]

    def append_row_to_df(self, row):
        self.candle_df.loc[len(self.candle_df)] = row

    def update_dataset(self, row):
        self.append_row_to_df(row)
        self.candle_df.drop([0])

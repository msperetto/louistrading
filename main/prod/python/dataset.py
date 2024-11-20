import pandas as pd
from prod.python.binance import Binance as binance
from common.python import database_operations as db

class Dataset():
    def __init__(self, pair, interval, startTime, endTime):
        self.pair = pair
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime
    
    def populate_initial_kline(self):
        self.dataset = binance().get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)

    def new_row(self):
        return binance().get_kline(self.pair, self.interval, None, None, 2).iloc[0]


from collections import OrderedDict
from prod.python.tradingBot import TradingBot
from common.python import database_operations as db
from prod.python.env_setup import Env_setup
from prod.python.candle_data import CandleData
from common.python.strategy import *
from prod.python.login import Login
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd

class Main():
    def __init__(self):
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config["max_open_orders"], base_config["order_value"], base_config["max_risk"], base_config["opperation_active"], base_config["leverage_long_value"], base_config["leverage_short_value"])
        self.exchange_session = Login("binance")
        self.exchange_session.login_database()
        self.strategies = [Strategy_Test()]

    def start(self):
        TradingBot(self.strategies, db, self.setup, self.exchange_session).run()
    
if __name__ == "__main__":
    Main().start()


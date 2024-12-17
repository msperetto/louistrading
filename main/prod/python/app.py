from collections import OrderedDict
from common.python import database_operations as db
from noshirt import NoShirt
from env_setup import Env_setup
from candle_data import CandleData
from common.python.strategy import *
from prod.python.login import Login
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd

class Main():
    def __init__(self):
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config["max_open_orders"], base_config["order_value"], base_config["max_risk"], base_config["opperating"])
        self.exchange_session = Login("binance")
        self.exchange_session.login_database()
        self.strategies = [Strategy_B1()]

    # def initialize_dataset(self):
        # pass
    
    def run(self):
        # call TradingBot here
        pass


    Main().run()


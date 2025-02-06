from collections import OrderedDict
from prod.tradingBot import TradingBot
from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.candle_data import CandleData
from prod.released_strategies.strategy_B2 import Strategy_B2
from prod.login import Login
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

#  TODO: 
class Main():
    def __init__(self):
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config["max_open_orders"], base_config["order_value"], base_config["max_risk"], base_config["opperation_active"], base_config["leverage_long_value"], base_config["leverage_short_value"])
        self.exchange_session = Login("binance")
        self.exchange_session.login_database()
        self.strategies = [Strategy_B2()]

    def start(self):
        print("Running...")
        logger.info(f"Start method - begin")
        TradingBot(self.strategies, db, self.setup, self.exchange_session).run()
    
if __name__ == "__main__":
    Main().start()


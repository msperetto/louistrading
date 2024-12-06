from common.python import database_operations as db
from noshirt import NoShirt
from env_setup import Env_setup
from ohcl import Ohcl
from common.python.strategy import *


#todo calculate logic to get start date to ohcl_df (get now - biggest interval for trend indicators times strategy candle interval)
class Main():
    def __init__(self):
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config["max_open_orders"], base_config["order_value"], base_config["max_risk"], base_config["opperating"])

    # def initialize_dataset(self):
        # pass
    
    def run_noshirt(self):
        # print(type(self.setup.active_pairs[0]))
        self.open_order_pairs = db.get_open_orders()
        for pair in self.setup.active_pairs:
            if pair not in self.open_order_pairs:
                strategy = Strategy_B1()
                df = Ohcl(pair, strategy.intraday_interval, "01.11.2024")
                df.populate_ohlc()
                manager = NoShirt(df.ohcl_df, strategy)
                manager.run()

Main().run_noshirt()


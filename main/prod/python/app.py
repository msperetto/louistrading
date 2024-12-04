from common.python import database_operations as db
from noshirt import NoShirt
from env_setup import Env_setup
from dataset import Dataset
from common.python.strategy import *

class Main():
    def __init__(self):
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config["max_open_orders"], base_config["order_value"], base_config["max_risk"], base_config["opperating"])

    def initialize_dataset(self):
        pass
    
    def run_noshirt(self):
        for pair in self.setup.active_pairs:
            df = Dataset("BTCUSDT", "1h", "01.11.2024", "30.11.2024")
            df.populate_ohlc()
            NoShirt(df.dataset, Strategy_B1())

Main().run_noshirt()


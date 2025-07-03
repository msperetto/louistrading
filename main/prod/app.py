from common.util import import_all_strategies
from common import STRATEGIES_MODULE_PROD, STRATEGIES_PATH_PROD
from prod.tradingBot import TradingBot
from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.released_strategies.strategy_B2 import Strategy_B2
from prod.login import Login
import logging
from prod import logger


#  TODO: 
class Main():
    def __init__(self):
        # Import all strategies from the released strategies folder.
        import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())

        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config)
        self.exchange_session = Login("binance")
        self.exchange_session.login_database()
        self.strategies = [Strategy_B2(), Strategy_SH7()]

        self.bot = TradingBot(self.strategies, db, self.setup, self.exchange_session)

    def start(self):
        print("Running...")
        logger.info(f"Start method - begin")
        self.bot.run()
    
if __name__ == "__main__":
    Main().start()


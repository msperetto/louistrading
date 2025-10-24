from common.util import import_all_strategies, get_strategies_by_type
from common import STRATEGIES_MODULE_PROD, STRATEGIES_PATH_PROD
from common.domain.strategy import Strategy
from prod.tradingBot import TradingBot
from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.login import Login
import logging
from prod import logger
from common.enums import Account_Operation_Type, Strategy_Operation_Type
from config.config import ACCOUNT_ID, ACCOUNT_ID_DELIST


class Main():
    def __init__(self):
        # Import all strategies from the released strategies folder.
        import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())

        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config)
        self.exchange_session_trading = Login("binance", Account_Operation_Type.TRADING, ACCOUNT_ID)
        self.exchange_session_trading.login_database()

        
        self.strategies_trading = get_strategies_by_type(Strategy_Operation_Type.TRADING, globals())

        self.bot = TradingBot(self.strategies_trading, db, self.setup, self.exchange_session_trading)


    def start(self):
        print("Running...")
        logger.info(f"Start method - begin")
        self.bot.run()
    
if __name__ == "__main__":
    Main().start()


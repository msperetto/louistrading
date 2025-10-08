from common.util import import_all_strategies, get_strategies_by_type
from common import STRATEGIES_MODULE_PROD, STRATEGIES_PATH_PROD
from prod.delist import Delist
from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.login import Login
import logging
from prod import delist_logger as logger
from common.enums import Account_Operation_Type, Strategy_Operation_Type
from config.config import ACCOUNT_ID_DELIST


class DelistMain():
    def __init__(self):
        # Import all strategies from the released strategies folder.
        import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())
        
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config)
        
        # Login for delist operations
        self.exchange_session_delist = Login("binance", Account_Operation_Type.DELIST, ACCOUNT_ID_DELIST)
        self.exchange_session_delist.login_database()
        
        # Get delist strategies
        self.strategies_delist = get_strategies_by_type(Strategy_Operation_Type.DELIST, globals())
        
        # Initialize delist handler with the first strategy
        if self.strategies_delist:
            self.delist_handler = Delist(self.strategies_delist[0], self.exchange_session_delist)
            self.delist_handler.setup = self.setup
        else:
            logger.error("No delist strategies found. Cannot initialize delist handler.")
            raise ValueError("No delist strategies available")


    def start(self):
        logger.info(f"Delist service started")
        self.delist_handler.run()
    
if __name__ == "__main__":
    DelistMain().start()

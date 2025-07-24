from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.login import Login
import logging
from prod import test_logger as logger
from prod.binance import Binance


#  TODO: 
class Main():
    def __init__(self):
        # Import all strategies from the released strategies folder.
        import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())


        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config)
        self.exchange_session = Login("binance")
        self.exchange_session.login_database()

        self.exchange_id = self.exchange_session.e_id
        self.exchange_sk = self.exchange_session.e_sk

        binance_response = Binance().get_account_info(self.exchange_id, self.exchange_sk)
        
    def start(self):
        logger.info(f"Binance resopnse: {self.binance_response}")
    
if __name__ == "__main__":
    Main().start()

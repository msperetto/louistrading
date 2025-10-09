from common.util import import_all_strategies
from common import STRATEGIES_MODULE_PROD, STRATEGIES_PATH_PROD
from prod.update_account_balances import UpdateAccountBalances
from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.login import Login
from prod import account_balance_updater_logger as logger
from common.enums import Account_Operation_Type
from config.config import ACCOUNT_ID, ACCOUNT_ID_DELIST


class UpdateAccountBalancesMain():
    def __init__(self):
        
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config)
        
        # Create exchange sessions for both trading and delist accounts
        self.exchange_sessions = []
        
        # Trading account session
        self.exchange_session_trading = Login("binance", Account_Operation_Type.TRADING, ACCOUNT_ID)
        self.exchange_session_trading.login_database()
        self.exchange_sessions.append(self.exchange_session_trading)
        
        # Delist account session
        self.exchange_session_delist = Login("binance", Account_Operation_Type.DELIST, ACCOUNT_ID_DELIST)
        self.exchange_session_delist.login_database()
        self.exchange_sessions.append(self.exchange_session_delist)
        
        # Initialize account balance updater
        self.balance_updater = UpdateAccountBalances(self.exchange_sessions)

    def start(self):
        logger.info(f"Account balance updater service started")
        self.balance_updater.update_account_balances()
    
if __name__ == "__main__":
    UpdateAccountBalancesMain().start()

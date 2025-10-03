# script to automatically update Binance account balances in the database,
# to be run every hour in a loop
# as a separate process from the trading bot
import time
from config.config import ACCOUNT_ID, ACCOUND_ID_DELIST, BASE_LOCAL_URL
from common.dao import database_operations as db
from common.domain.account_balance import AccountBalance
from common.dao.account_balance_dao import get_account_balance, update_account_balance, insert_account_balance
from common.enums import Account_Operation_Type
from prod.binance import Binance
from prod import account_balance_updater_logger as logger

class UpdateAccountBalances:
    def __init__(self, exchange_sessions):
        self.exchange_sessions = exchange_sessions
        self.binance = Binance()

    def update_account_balances():
        """
        Update account balances in the database.
        """
        logger.info("Starting account balance update process.")
        
        while True:
            try:
                # Fetch current balances from Binance
                balances = self._get_current_balances()
                timestamp = int(time.time() * 1000)  # Current time in milliseconds
                
                for balance in balances:
                    account_id = balance["account_id"]
                    account_balance = balance["balance"]
                    operation_type = balance["operation_type"]
                    
                    existing_balance = get_account_balance(account_id)
                    
                    if existing_balance:
                        update_account_balance(account_id, account_balance, margin_ratio=2)  # Assuming margin_ratio is 2 for simplicity
                        logger.info(f"Updated balance for account {account_id} ({operation_type}): {account_balance} USDT")
                    else:
                        insert_account_balance(account_id, account_balance, margin_ratio=2)  # Assuming margin_ratio is 2 for simplicity
                        logger.info(f"Inserted new balance for account {account_id} ({operation_type}): {account_balance} USDT")
            except Exception as e:
                logger.error(f"Error updating account balances: {e}")
            
            # Wait for one hour before next update
            time.sleep(3600)

    def _get_current_balances(self):
        balances = []
        for exchange_session in self.exchange_sessions:
            account_balance = float(self.binance.get_account_info(exchange_session.e_id, exchange_session.e_sk)["availableBalance"])
            account_balance_dao.update_account_balance(exchange_session.account_id, account_balance, self.margin_ratio)
            #append a dictionary with operation type and balance:
            balances.append({"account_id": exchange_session.account_id, "operation_type": exchange_session.account_operation_type, "balance": account_balance})
        return balances
            
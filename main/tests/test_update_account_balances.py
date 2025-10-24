from prod.update_account_balances import UpdateAccountBalances
from prod.login import Login
from config.config import ACCOUNT_ID, ACCOUNT_ID_DELIST

# This is a true integration test, not a unit test.
# It is using real login sessions and a real Binance API connection.
# It is also updating the database.
# As it is a db table intended to be updated every hour, it is not a problem.
# Just make sure to check the logs and the db table to see if everything is working fine
# The test will run in a loop every 1 hour, so you can stop it anytime.

class TestUpdateAccountBalances():
    def test_update_account_balances(self):
        trading_session = Login("binance", "TRADING", ACCOUNT_ID)
        trading_session.login_database()
        delist_session = Login("binance", "DELIST", ACCOUNT_ID_DELIST)
        delist_session.login_database()

        exchange_sessions = [trading_session, delist_session]

        updater = UpdateAccountBalances(exchange_sessions)
        balances = updater._get_current_balances()

        # Check balances structure
        self.assertEqual(len(balances), 2)
        self.assertTrue(all("balance" in b for b in balances))

        updater.update_account_balances()

if __name__ == "__main__":
    TestUpdateAccountBalances().test_update_account_balances()
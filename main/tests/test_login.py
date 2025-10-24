# Create login test file to create and update binance login sessions in the database
# to be used by the trading bot, delist and the account balance updater
from config.config import ACCOUNT_ID, ACCOUNT_ID_DELIST, BASE_LOCAL_URL
from common.enums import Account_Operation_Type
from prod.login import Login

def test_login():
    exchange_session = Login("binance", Account_Operation_Type.DELIST)
    exchange_session.login_database()

if __name__ == "__main__":
    test_login()

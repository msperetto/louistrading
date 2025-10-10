import logging
from common.enums import Environment_Type

# Connection string for the database
DEV_ENV_CON = "host=db dbname=noshirt user=postgres password=postgres"

# Create a db postgres connection on hostname/address: 16.171.16.170, port: 5431, name: marlin, username: postgres, password: postgres
# DEV_ENV_CON = "host=
MARLIN_DB_CON = "host=16.171.16.170 port=5431 dbname=noshirt user=postgres password=postgres"

# Defining environment
NEGOCIATION_ENV =  Environment_Type.PROD

# Test mode for delist announcements (when NEGOCIATION_ENV is TEST)
USE_TEST_ANNOUNCEMENTS = True  # Set to False to use real Binance data even in TEST mode

# Base URL for local API
BASE_LOCAL_URL = "http://localhost:8000/"

# Log level configuration
LOG_LEVEL = logging.DEBUG  # It can be: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Defining user account id
ACCOUNT_ID = 1
ACCOUNT_ID_DELIST = 2

# Defining if the system will utilize STOP orders
USE_STOP_ORDERS = True  # Set to False if you do not want to use stop orders

# Defining the STOP LOSS percentage
STOP_LOSS_PERCENTAGE = 0.02  # 2%

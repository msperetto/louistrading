import logging
from common.enums import Environment_Type

# Connection string for the database
DEV_ENV_CON = "host=db dbname=noshirt user=postgres password=postgres"

# Definig environment
NEGOCIATION_ENV =  Environment_Type.PROD

# Base URL for local API
BASE_LOCAL_URL = "http://localhost:8000/"

# Log level configuration
LOG_LEVEL = logging.DEBUG  # It can be: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Defining user account id
ACCOUNT_ID = 1

# Defining if the system will utilize STOP orders
USE_STOP_ORDERS = True  # Set to False if you do not want to use stop orders

# Defining the STOP LOSS percentage
STOP_LOSS_PERCENTAGE = 0.02  # 2%

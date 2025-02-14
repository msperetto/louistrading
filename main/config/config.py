import logging
from common.enums import Environment_Type

# Connection string for the database
DEV_ENV_CON = "host=db dbname=noshirt user=postgres password=postgres"

# Definig environment
NEGOCIATION_ENV =  Environment_Type.BACKTEST

# Log level configuration
LOG_LEVEL = logging.DEBUG  # It can be: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Defining user account id
ACCOUNT_ID = 1

# Strategies Folder:
STRATEGIES_MODULE = "common.strategies"

# Strategies Path:
STRATEGIES_PATH = Path(__file__).parent.parent / 'common' / 'strategies'

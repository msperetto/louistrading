import logging
from common.enums import Environment_Type

# Connection string for the database
# DEV_ENV_CON = "dbname=noshirt user=peretto"
DEV_ENV_CON = "host=db dbname=noshirt user=postgres password=@tkTYB9i"

# Definig environment
NEGOCIATION_ENV =  Environment_Type.BACKTEST

# Log level configuration
LOG_LEVEL = logging.DEBUG  # It can be: DEBUG, INFO, WARNING, ERROR, CRITICAL

from enum import Enum

class Json_type(Enum):
    INTRADAY  = 1
    STRATEGY = 2
    PORTFOLIO = 3

class Backtest_manager_type(Enum):
    INTRADAY  = 1
    STRATEGY = 2
    PORTFOLIO = 3
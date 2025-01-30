from enum import Enum

class Environment_Type(str, Enum):
    BACKTEST = "BACKTEST"
    TEST = "TEST"
    PROD = "PROD"

class Operation_Type(str, Enum):
    ENTRY = "Entry"
    CLOSE = "Close"

class Side_Type(str, Enum):
    LONG = "long"
    SHORT = "short"
from enum import Enum

class Environment_Type(str, Enum):
    BACKTEST = "BACKTEST"
    TEST = "TEST"
    PROD = "PROD"

class Operation_Type(str, Enum):
    ENTRY = "Entry"
    CLOSE = "Close"
    STOP = "Stop"

class Side_Type(str, Enum):
    LONG = "BUY"
    SHORT = "SELL"

class Alert_Level(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# This enum is only utilized in the docker compose files to automatically 
# identify if the bot is running in a local or AWS environment.
# So if we want to update it, we need to update the docker compose files as well.
class Environment_Place(str, Enum):
    LOCAL = "LOCAL"
    AWS = "AWS"
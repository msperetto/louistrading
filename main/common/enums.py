from enum import Enum

class Environment_Type(str, Enum):
    BACKTEST = "BACKTEST"
    TEST = "TEST"
    PROD = "PROD"

class Operation_Type(str, Enum):
    ENTRY = "Entry"
    CLOSE = "Close"

class Side_Type(str, Enum):
    LONG = "BUY"
    SHORT = "SELL"

# This enum is only utilized in the docker compose files to automatically 
# identify if the bot is running in a local or AWS environment.
# So if we want to update it, we need to update the docker compose files as well.
class Environment_Place(str, Enum):
    LOCAL = "LOCAL"
    AWS = "AWS"
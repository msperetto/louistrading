from enum import Enum

class Json_type(Enum):
    INTRADAY  = 1
    STRATEGY = 2
    PORTFOLIO = 3
    INTRADAY_TREND = 4

class BacktestSplitMode(Enum):
    FULL = 1         # Run the entire period without partitioning
    MONTHLY = 2      # Divide month by month
    CUSTOM_DAYS = 3  # Divide by X days, using another parameter (e.g., split_days = 7)
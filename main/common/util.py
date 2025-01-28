from config.config import NEGOCIATION_ENV
from common.enums import *


def get_value_by_index(series, index):
    """
    Returns the value at the specified position in the series depending on the environment.
    Includes "iloc" in case it's not BACKTEST.
    """
    if NEGOCIATION_ENV == Environment_Type.BACKTEST:
        return series[index]
    return series.iloc[index]
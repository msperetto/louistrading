from config.config import NEGOCIATION_ENV
from common.enums import *
from common.strategyLong import StrategyLong
from common.strategyShort import StrategyShort
import importlib
import pkgutil


def get_value_by_index(series, index):
    """
    Returns the value at the specified position in the series depending on the environment.
    Includes "iloc" in case it's not BACKTEST.
    """
    if NEGOCIATION_ENV == Environment_Type.BACKTEST:
        return series[index]
    return series.iloc[index]

# Dynamically import all modules from the strategies folder
def import_all_strategies(strategies_path, strategies_module, caller_globals):
    for module_info in pkgutil.iter_modules([str(strategies_path)]):
        module = importlib.import_module(f"{strategies_module}.{module_info.name}")
        caller_globals.update({name: cls for name, cls in module.__dict__.items() if isinstance(cls, type)})

# Returns the Side_Type based on the type of the given strategy.
def get_side(strategy):
    SIDE_MAPPING = {
        StrategyLong: Side_Type.LONG,
        StrategyShort: Side_Type.SHORT
    }
    return SIDE_MAPPING.get(strategy.__class__.__bases__[0])
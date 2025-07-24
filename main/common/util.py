from config.config import NEGOCIATION_ENV
from common.enums import *
from common.strategyLong import StrategyLong
from common.strategyShort import StrategyShort
import importlib
import pkgutil
import os
from prod import logger, aws_logger
from typing import List, Dict
from prod.binance import Binance


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

# Returns the Side_Type based on the type of the given strategy (looks for the mother class of the strategy).
# If the strategy is closing, it returns the opposite side.
def get_side(strategy, closing=False):
    SIDE_MAPPING = {
        StrategyLong: Side_Type.LONG.value,
        StrategyShort: Side_Type.SHORT.value
    }
    base_class = strategy.__class__.__bases__[0]
    if closing:
        if base_class == StrategyLong:
            side = Side_Type.SHORT.value
        elif base_class == StrategyShort:
            side = Side_Type.LONG.value
    else:
        side = SIDE_MAPPING.get(base_class)
    if side is None:
        logging.warning(f"Unknown strategy base class: {base_class.__name__}")
    return side

def get_server_public_ip(server_ip_name):
    try:
        env_ip = os.getenv(server_ip_name)
        if env_ip:
            aws_logger.debug(f"retrieved {server_ip_name} from environment variable: {env_ip}")
            return env_ip.strip()
        aws_logger.warning(f"{server_ip_name} environment variable not set")
        return None
    except Exception as e:
        aws_logger.error(f"Error retrieving public IP: {e}")
        return None

def get_pairs_precision(pairs: List) -> Dict:
    """
    Returns the precision of the given list of pairs.
    So when passing the quantity of an order to the exchange, the decimal places are correct.
    """
    precision_result = {}
    try:
        exchange_info = Binance().get_exchange_info()
        for pair in pairs:
            pair_result = {pair: symbol['quantityPrecision'] for symbol in exchange_info['symbols'] if symbol['symbol'] == pair}
            if pair_result:
                precision_result.update(pair_result)
            else:
                logger.warning(f"Pair {pair} not found in exchange info.")
        return precision_result

    except Exception as e:
        logger.error(f"Error retrieving precision for {pair}: {e}")
        return None
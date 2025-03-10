from pathlib import Path

# Backtest Strategies Folder:
STRATEGIES_MODULE_BT = "common.strategies"

# Backtest Strategies Path:
STRATEGIES_PATH_BT = Path(__file__).parent.parent / 'common' / 'strategies'

# Prod Strategies Folder:
STRATEGIES_MODULE_PROD = "prod.released_strategies"

# Prod Strategies Path:
STRATEGIES_PATH_PROD = Path(__file__).parent.parent / 'prod' / 'released_strategies'

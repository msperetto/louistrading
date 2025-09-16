from common.util import import_all_strategies
from common import STRATEGIES_MODULE_PROD, STRATEGIES_PATH_PROD
from common.dao.strategy_dao import get_enabled_strategies_by_type
from common.domain.strategy import Strategy
from prod.tradingBot import TradingBot
from common.dao import database_operations as db
from prod.env_setup import Env_setup
from prod.login import Login
import logging
from prod import logger
from common.enums import Account_Operation_Type, Strategy_Operation_Type


class Main():
    def __init__(self):
        # Import all strategies from the released strategies folder.
        import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())


        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config)
        self.exchange_session = Login("binance", Account_Operation_Type.TRADING)
        self.exchange_session.login_database()
        
        self.strategies_trading = self._get_strategies_by_type(Strategy_Operation_Type.TRADING)


        self.bot = TradingBot(self.strategies, db, self.setup, self.exchange_session)

    def _get_strategies_by_type(self, operation_type:str):
        """
        Gets from DB all trading enabled strategies classes names and instantiates it.
        Returns:
            list of Strategy objects
        """
        strategies: list[Strategy] = get_enabled_strategies_by_type(operation_type)
        strategy_objects = []
        for strategy in strategies:
            try:
                strategy_class = globals()[strategy.name]
                strategy_instance = strategy_class()
                strategy_objects.append(strategy_instance)
                logger.info(f"Strategy {strategy.name} instantiated successfully.")
            except KeyError as e:
                logger.error(f"Strategy class '{strategy.name}' not found: {e}")
            except Exception as e:
                logger.error(f"Error instantiating strategy '{strategy.name}': {e}")
        return strategy_objects

    def start(self):
        print("Running...")
        logger.info(f"Start method - begin")
        self.bot.run()
    
if __name__ == "__main__":
    Main().start()


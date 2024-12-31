import time
from datetime import datetime, timedelta
from collections import OrderedDict
from common.python import database_operations as db
from common.python import management
from prod.python.dataset import Dataset
from prod.python.strategy_manager import StrategyManager
from prod.python.env_setup import Env_setup
from prod.python.candle_data import CandleData
from common.python.strategy import *
from prod.python.login import Login
import pandas as pd
from prod.python.tests.negociation_main_tests import TestNegociationMain
import os
import logging
import time

# Configure logging
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'trading_bot.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, strategies, db, setup, exchange_session):
        self.strategies = strategies
        self.db = db
        self.setup = setup
        self.exchange_session = exchange_session
        # dict to track last execution by pair and strategy. Dict structure: { (pair, strategy): datetime }
        self.last_executions = {}
        self.active_pairs = []
        self.pairs = []
        self.opened_trade_pairs = []

    def run(self):

        while True:
            # Handle opened trades. Check if it's ready to close postion.
            self.handle_opened_trades()

            self.handle_new_trades()

            # Pause the loop for 1 minute before trying again
            time.sleep(60)

    def create_combined_dataset(self, pair, strategy):
        #calculating de date for the first candle of the dataset
        start_date = management.calc_start_date(strategy)

        #getting intraday candle dataset from binance
        intraday_data = CandleData(pair, strategy.intraday_interval, start_date, "intraday")
        intraday_data.populate_data(round(time.time()*1000))
        
        #adding strategy indicators to intraday dataset
        intraday_dataset = Dataset(intraday_data.candle_df, strategy)
        intraday_dataset.add_indicators_to_candle_dataset("intraday")

        #getting trend candle dataset from binance
        trend_data = CandleData(pair, strategy.trend_interval, start_date, "trend")
        trend_data.populate_data(round(time.time()*1000))

        #adding strategy indicators to trend dataset
        trend_dataset = Dataset(trend_data.candle_df, strategy)
        trend_indicators_list = trend_dataset.add_indicators_to_candle_dataset("trend")

        #merging intraday and trend datasets in one final dataset
        return intraday_dataset.merge_dataframes(trend_dataset.dataset, *trend_indicators_list)


    def handle_new_trades(self):
        # Check if the bot is active
        if not self.setup.opperation_active:
            return

        self.active_pairs = self.db.get_active_pairs()

        #as the get_open_trade_pairs returns 2 values, just get the first one(pair)
        opened_trade_pairs = [pair[0] for pair in self.db.get_open_trade_pairs()]

        # TODO: get pairs with opened alerts

        # Select eligible pairs.
        # Pairs that are active, do not have any opened position and do not have any opened alert.
        self.pairs = [pair for pair in self.active_pairs if pair not in opened_trade_pairs]

        for pair in self.pairs:
            for strategy in self.strategies:
                # Check if the strategy has been executed recently
                if not self.should_run_strategy(pair, strategy):
                    # Jump to the next strategy for this pair.
                    continue

                # Updates the last run time
                self.last_executions[(pair, strategy)] = datetime.now()
                final_dataset = self.create_combined_dataset(pair, strategy)

                #logging for debugging
                logger.info(f"TRYING TO OPEN POSITION")
                logger.debug(f"Pair: {pair} - datetime: {datetime.now()} - final_dataset:\n{final_dataset}")

                manager = StrategyManager(
                    pair,
                    final_dataset,
                    self.exchange_session.e_id,
                    self.exchange_session.e_sk,
                    self.setup.order_value,
                    strategy
                )
                manager.try_open_position()


    def handle_opened_trades(self):
        # Handle opened trades. Check if we is ready to sell.
        self.opened_trade_pairs = db.get_open_trade_pairs()
        for pair, trade_id in self.opened_trade_pairs:
            # get the strategy class object (not only the name as string)
            strategy = globals().get(db.get_strategy_name(db.get_open_trade_strategy(pair)))
            #instantiate the strategy class:
            strategy = strategy()
            
            final_dataset = self.create_combined_dataset(pair, strategy)

            #logging for debugging
            logger.info(f"TRYING TO CLOSE POSITION")
            logger.debug(f"Pair: {pair} - datetime: {datetime.now()} - final_dataset:\n{final_dataset}")

            manager = StrategyManager(
                pair,
                final_dataset,
                self.exchange_session.e_id,
                self.exchange_session.e_sk,
                self.setup.order_value,
                strategy
            )
            manager.try_close_position(strategy, trade_id)


    def should_run_strategy(self, pair, strategy):
        """
        Check whether the strategy should be executed based on the interval.
        """
        last_execution = self.last_executions.get((pair, strategy))
        # If it has never been run, it should run.
        if not last_execution:
            return True

        # Calculates the minimum required interval.
        now = datetime.now()

        # First convert "strategy.intraday_interval" and "strategy.trend_interval" to the same base period. In this case, minutes.
        intraday_interval = management.time_intervals_to_minutes(strategy.intraday_interval)

        # The next time the strategy can be executed.
        # The solution below it works only when intraday_interval is at least 1h. If the interval is minutes, then it won't work.
        next_execution_time = last_execution + timedelta(minutes=intraday_interval)
        next_execution_time = next_execution_time.replace(minute=0, second=0)

        # Only executes if the required time has already passed.
        return now > next_execution_time
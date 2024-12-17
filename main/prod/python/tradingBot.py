import time
from datetime import datetime, timedelta
from collections import OrderedDict
from common.python import database_operations as db
from common.python import management
from dataset import Dataset
from strategy_manager import StrategyManager
from env_setup import Env_setup
from candle_data import CandleData
from common.python.strategy import *
from prod.python.login import Login

class TradingBot:
    def __init__(self, strategies, db, setup, exchange_session):
        self.strategies = strategies
        self.db = db
        self.setup = setup
        self.exchange_session = exchange_session
        # dict to track last execution by pair and strategy. Dict structure: { (pair, strategy): datetime }
        self.last_executions = {}

    def run(self):
        while True:
            # Handle opened trades. Check if it's ready to close postion.
            # self.handle_opened_trades()

            self.handle_new_trades()

            # Pause the loop for 1 minute before trying again
            time.sleep(60)

    def handle_new_trades(self):
        # Check if the bot is active
        if not self.setup.opperating:
            return

        self.active_pairs = self.db.get_active_pairs()
        open_orders = self.db.get_open_orders()
        # TODO: get pairs with opened alerts

        # Select eligible pairs.
        # Pairs that are active, do not have any opened position and do not have any opened alert.
        self.pairs = [pair for pair in self.active_pairs if pair not in open_orders]

        for pair in self.pairs:
            for strategy in self.strategies:
                # Check if the strategy has been executed recently
                if not self.should_run_strategy(pair, strategy):
                    # Jump to the next strategy for this pair.
                    continue

                # Updates the last run time
                self.last_executions[(pair, strategy)] = datetime.now()

                # Main logic of the strategy
                start_date = management.calc_start_date(strategy)

                #getting intraday candle dataset from binance
                intraday_data = CandleData(pair, strategy.intraday_interval, start_date)
                intraday_data.populate_data()
                
                #adding strategy indicators to intraday dataset
                intraday_dataset = Dataset(intraday_data.candle_df, strategy)
                intraday_dataset.add_indicators_to_candle_dataset("intraday")

                #getting trend candle dataset from binance
                trend_data = CandleData(pair, strategy.trend_interval, start_date)
                trend_data.populate_data()

                #adding strategy indicators to trend dataset
                trend_dataset = Dataset(trend_data.candle_df, strategy)
                trend_indicators_list = trend_dataset.add_indicators_to_candle_dataset("trend")

                #merging intraday and trend datasets in one final dataset
                final_dataset = intraday_dataset.merge_dataframes(trend_dataset.dataset, *trend_indicators_list)
                manager = StrategyManager(
                    pair,
                    final_dataset,
                    self.exchange_session.e_id,
                    self.exchange_session.e_sk,
                    self.setup.order_value,
                    strategy
                )
                manager.run()


    def handleOpenedTrades(self):
        # Handle opened trades. Check if we is ready to sell.
        self.opened_trades = db.get_open_orders()
        for trade in self.opened_trades:
            # get necessary information from the trade object.
            strategy = trade.strategy
            pair = trade.pair

            candleData = CandleData(pair, strategy.intraday_interval, ...)
            candleData.populate_values()

            manager = StrategyManager(..., strategy)
            manager.checkClosePosition()


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
        trend_interval = management.time_intervals_to_minutes(strategy.trend_interval)
        interval = max(intraday_interval, trend_interval)

        # The next time the strategy can be executed.
        next_execution_time = last_execution + timedelta(minutes=interval)

        # Only executes if the required time has already passed.
        return now >= next_execution_time

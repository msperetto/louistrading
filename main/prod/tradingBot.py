import time
from datetime import datetime, timedelta
from collections import OrderedDict
from common.dao import strategy_dao, trade_dao, account_balance_dao, alert_dao
from common.dao import database_operations as db
from common import management
from prod.dataset import Dataset
from prod.strategy_manager import StrategyManager
from common.util import import_all_strategies
from common import STRATEGIES_MODULE_PROD, STRATEGIES_PATH_PROD
from prod.env_setup import Env_setup
from prod.candle_data import CandleData
from common.strategy import *
from common.strategyLong import StrategyLong
from common.strategyShort import StrategyShort
from prod.login import Login
import pandas as pd
from tests.negociation_main_tests import TestNegociationMain
from common.dao import alert_dao as alert_db
from prod.binance import Binance
import os
import logging
import time
from config.config import NEGOCIATION_ENV, ACCOUNT_ID, USE_STOP_ORDERS
from common.enums import Environment_Type, Alert_Level
from prod import logger
from common.util import get_pairs_precision, get_pairs_price_precision
from prod import notify
from prod.negotiate import Negotiate
from marlinStop.stopLogic import StopManager


class TradingBot:

    MINIMUM_BALANCE_INCREMENT = 1.2

    def __init__(self, strategies, db, setup, exchange_session):
        # Import all strategies from the released strategies folder.
        import_all_strategies(STRATEGIES_PATH_PROD, STRATEGIES_MODULE_PROD, globals())

        self.strategies = strategies
        self.db = db
        self.setup = setup
        self.exchange_session = exchange_session
        # dict to track last execution by pair and strategy. Dict structure: { (pair, strategy): datetime }
        self.last_executions = {}
        # TODO: get margin ratio correctly from the exchange
        self.margin_ratio = 2
        
        self.current_balance = self._get_current_balance()
        # if account balance is not registered in db, insert it, else update it
        if account_balance_dao.get_account_balance(ACCOUNT_ID) is None:
            account_balance_dao.insert_account_balance(ACCOUNT_ID, self.current_balance, self.margin_ratio)
        else:
            account_balance_dao.update_account_balance(ACCOUNT_ID, self.current_balance, self.margin_ratio)
        self.running = True
        self.stopped = False # variable to control if the bot is fully stopped, so we can handle the shutdown/hardreset process correctly 

        # setting binance initial leverage value
        for pair in self.db.get_active_pairs():
            self._set_leverage(pair, self.setup.leverage_long_value)

        # getting decimal precision by pair:
        self.pairs_precision = get_pairs_precision(self.db.get_active_pairs())
        self.pairs_price_precision = get_pairs_price_precision(self.db.get_active_pairs())

    def stop(self):
        logger.info("Stopping bot...")
        self.running = False
    
    def start(self):
        logger.info("Starting bot...")
        self.running = True

    def run(self):
        while self.running:
            try:
                self.stopped = False
                # register execution time to monitor bot alive status:
                db.update_bot_execution_control()

                # Handle opened trades. Check if it's ready to close postion.
                self.handle_opened_trades()

                self.handle_new_trades()

                # Pause the loop for 1 minute before trying again
                time.sleep(2)
                logger.debug(f"Bot running after sleep. self.stopped: {self.stopped}")
                logger.debug(f"Bot running status: {self.running}")
                while not self.running:
                    logger.info("Bot is paused. Waiting for 20 seconds...")
                    self.stopped = True
                    logger.debug(f"Bot stopped status: {self.stopped}")
                    print("Bot is paused. Waiting for 20 seconds...")
                    time.sleep(20)
            except Exception as e:
                notify.send_message_alert(
                    f"An error occurred in the bot main loop(run): \n {e}. \n Please check the logs for more details."
                )
                logger.error(f"An error occurred: {e}")
                logger.info("Retrying in 2 minutes...")
                time.sleep(120)

    def create_combined_dataset(self, pair, strategy):
        # calculating de date for the first candle of the dataset
        start_date = management.calc_start_date(strategy)

        # getting intraday candle dataset from binance
        intraday_data = CandleData(
            pair, strategy.intraday_interval, start_date, "intraday")
        intraday_data.populate_data(round(time.time()*1000))

        # adding strategy indicators to intraday dataset
        intraday_dataset = Dataset(intraday_data.candle_df, strategy)
        intraday_dataset.add_indicators_to_candle_dataset("intraday")

        # getting trend candle dataset from binance
        trend_data = CandleData(
            pair, strategy.trend_interval, start_date, "trend")
        trend_data.populate_data(round(time.time()*1000))

        # adding strategy indicators to trend dataset
        trend_dataset = Dataset(trend_data.candle_df, strategy)
        trend_indicators_list = trend_dataset.add_indicators_to_candle_dataset(
            "trend")

        #merging intraday and trend datasets in one final dataset
        return intraday_dataset.merge_dataframes(trend_dataset.dataset, *trend_indicators_list)


    def handle_new_trades(self):
        logger.debug(f"handle_new_trades - begin")
        # Check if the bot is active
        if not self.setup.opperation_active:
            return

        # Check balance; Stop new trades if balance is below the minimum required.
        if self._is_balance_below_minimum():
            logger.info(f"Current balance is below the minimum required. Current balance: {self.current_balance}")
            return

        active_pairs = self.db.get_active_pairs()

        opened_trades = trade_dao.get_open_trade_pairs()
        opened_trade_pairs = [trade.pair for trade in opened_trades]

        # Number of available orders to open
        available_orders = self.setup.max_open_orders - len(opened_trade_pairs)

        active_alerts_pairs = [alert.pair for alert in alert_db.get_active_alerts()]

        # Select eligible pairs.
        # Pairs that are active, do not have any opened position and do not have any opened alert.
        pairs = [pair for pair in active_pairs if pair not in opened_trade_pairs and pair not in active_alerts_pairs]

        # TODO: What if an exception occurs inside on one of the for loops?
        # Do we want to continue the next pair and strategy?
        for pair in pairs:
            # Check if opened orders limit has been reached (using break because cannot open more orders)
            if available_orders == 0:
                break

            for strategy in self.strategies:

                # TODO: Checar "saldo" (talvez collateral) numa tabela interna?.
                # Prevenir novas operações caso não tenha saldo suficiente.

                try:
                    
                    # Check if the strategy has been executed recently
                    if not self.should_run_strategy(pair, strategy):
                        # Jump to the next strategy for this pair.
                        continue
                        
                    logger.debug(f"handle_new_trades - pair: {pair} - strategy: {strategy}")
                    logger.debug(f"current balance: {self.current_balance}")

                    #Check balance; Stop new trades if balance is below the minimum required.
                    if self._is_balance_below_minimum():
                        logger.info(f"Current balance is below the minimum required. Current balance: {self.current_balance}")
                        return

                    # Updates the last run time
                    self._update_last_execution(pair, strategy)

                    final_dataset = self._prepare_final_dataset(pair, strategy)

                    #logging for debugging
                    logger.info(f"TRYING TO OPEN POSITION - Pair: {pair}")
                    logger.debug(f"Pair: {pair} - datetime: {datetime.now()} - final_dataset:\n{final_dataset}")

                    manager = StrategyManager(
                        pair,
                        self.pairs_precision[pair],
                        self.pairs_price_precision[pair],
                        final_dataset,
                        self.exchange_session.e_id,
                        self.exchange_session.e_sk,
                        self.setup.order_value,
                        strategy
                    )
                    if manager.try_open_position():
                        available_orders -= 1
                        self.current_balance = self._get_current_balance()
                        # If the position was opened, then jump to the next pair.
                        break
                except Exception as e:
                    logger.error(f"An error occurred while trying to open position for pair {pair} with strategy {strategy}: {e}")
                    alert_dao.insert_alert(
                        pair,
                        Alert_Level.ERROR,
                        True,
                        f"An error occurred while trying to open position for pair {pair} with strategy {strategy}: {e}"
                    )
                    # Notify the user about the error
                    notify.send_message_alert(
                        f"An error occurred while trying to open position for pair {pair} with strategy {strategy}: {e}"
                    )
                    continue


    def handle_opened_trades(self):
        # Handle opened trades. Check if we is ready to sell.
        logger.debug(f"handle_opened_trades - begin")

        opened_trades = trade_dao.get_open_trade_pairs()

        # TODO: What if an exception occurs in a specific trade?
        # We might want to continue processing the for loop and try to close the next trade. 
        for trade in opened_trades:
            try:
                # First check if current trade was closed by a stop order:
                if USE_STOP_ORDERS:
                    stop_manager = StopManager(trade.pair, self.pairs_price_precision[trade.pair], self.exchange_session.e_id, self.exchange_session.e_sk)
                    # transform trade.open_time to milliseconds
                    start_time = int(trade.open_time.timestamp() * 1000)
                    closed_stop_orders = stop_manager.check_closed_stop_order(trade.pair, start_time)
                    if closed_stop_orders:
                        # register and notify the user about the closed stop order
                        negotiate = Negotiate(
                            trade.pair,
                            self.pairs_precision[trade.pair],
                            self.pairs_price_precision[trade.pair],
                            self.exchange_session.e_id,
                            self.exchange_session.e_sk
                        )

                        negotiate.register_close_transaction(
                            closed_stop_orders[0],
                            trade.strategy_id,
                            trade.id,
                            "Stop"
                        )
                        # Go to the next opened trade
                        continue

                strategyObject = strategy_dao.get_strategy_by_id(trade.strategy_id)
                strategyClassName = globals().get(strategyObject.name)
                #instantiate the strategy class:
                strategy = strategyClassName()

                # Check if the strategy has been opened in the last candle
                if not self.should_run_strategy(trade.pair, strategy):
                    # Jump to the next opened trade.
                    continue

                logger.debug(f"handle_opened_trades - pair: {trade.pair}")
                logger.debug(f"current balance: {self.current_balance}")

                # Updates the last run time
                self._update_last_execution(trade.pair, strategy)

                final_dataset = self._prepare_final_dataset(trade.pair, strategy)

                #logging for debugging
                logger.info(f"TRYING TO CLOSE POSITION - Pair: {trade.pair}")
                logger.debug(f"Pair: {trade.pair} - datetime: {datetime.now()} - final_dataset:\n{final_dataset}")

                manager = StrategyManager(
                    trade.pair,
                    self.pairs_precision[trade.pair],
                    self.pairs_price_precision[trade.pair],
                    final_dataset,
                    self.exchange_session.e_id,
                    self.exchange_session.e_sk,
                    self.setup.order_value,
                    strategy
                )
                if manager.try_close_position(strategy, trade.id):
                    self.current_balance = self._get_current_balance()
            except Exception as e:
                logger.error(f"An error occurred while trying to close position for trade {trade.id}: {e}")
                alert_dao.insert_alert(
                    trade.pair,
                    Alert_Level.ERROR,
                    True,
                    f"An error occurred while trying to close position for trade {trade.id}: {e}"
                )
                notify.send_message_alert(
                    f"An error occurred while trying to close position for trade {trade.id}: {e}"
                )
                continue


    def should_run_strategy(self, pair, strategy):
        """
        Check whether the strategy should be executed based on the interval.
        """
        last_execution = self.last_executions.get((pair, strategy.__class__.__name__))
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

    def _prepare_final_dataset(self, pair, strategy):
        dataset = self.create_combined_dataset(pair, strategy)
        if NEGOCIATION_ENV == Environment_Type.TEST:
            return TestNegociationMain().add_fake_row(dataset)
        return dataset
    
    def _get_current_balance(self):
        account_balance = float(Binance().get_account_info(self.exchange_session.e_id, self.exchange_session.e_sk)["availableBalance"])
        account_balance_dao.update_account_balance(ACCOUNT_ID, account_balance, self.margin_ratio)
        return account_balance

    def _is_balance_below_minimum(self):
        return self.current_balance < (self.setup.order_value * self.MINIMUM_BALANCE_INCREMENT)

    def _set_leverage(self, pair, leverage):
        if NEGOCIATION_ENV == Environment_Type.PROD:
            Binance().change_initial_leverage(pair, int(leverage), self.exchange_session.e_id, self.exchange_session.e_sk)

    def _update_last_execution(self, pair, strategy):
        """
        Update the last execution time for the given pair and strategy.
        """
        self.last_executions[(pair, strategy.__class__.__name__)] = datetime.now()
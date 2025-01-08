import time
from datetime import datetime, timedelta
from collections import OrderedDict
from common.dao import strategy_dao, trade_dao
from common.dao import database_operations as db
from common import management
from prod.dataset import Dataset
from prod.strategy_manager import StrategyManager
from prod.env_setup import Env_setup
from prod.candle_data import CandleData
from common.strategy import *
from prod.login import Login
import pandas as pd
from tests.negociation_main_tests import TestNegociationMain
from common.dao import alert_dao as alert_db
import os
import logging
import time

logger = logging.getLogger(__name__)

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
            try:
                # Handle opened trades. Check if it's ready to close postion.
                self.handle_opened_trades()

                self.handle_new_trades()

                # Pause the loop for 1 minute before trying again
                time.sleep(60)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                logger.info("Retrying in 2 minutes...")
                time.sleep(120) 

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

        active_pairs = self.db.get_active_pairs()

        opened_trades = trade_dao.get_open_trade_pairs()
        opened_trade_pairs = [trade.pair for trade in opened_trades]

        active_alerts_pairs = [alert.pair for alert in alert_db.get_active_alerts()]

        # Select eligible pairs.
        # Pairs that are active, do not have any opened position and do not have any opened alert.
        pairs = [pair for pair in active_pairs if pair not in opened_trade_pairs and pair not in active_alerts_pairs]

        # TODO: What if an exception occurs inside on one of the for loops?
        # Do we want to continue the next pair and strategy?
        for pair in pairs:
            for strategy in self.strategies:

                # TODO: Checar "saldo" (talvez collateral) numa tabela interna?.
                # Prevenir novas operações caso não tenha saldo suficiente.

                # TODO: Checar se a qtd de trades ativos está dentro do limite permite (setup.max_open_orders).
                # Acredito que o jeito mais simples é fazer uma nova chamada na tabela de "trade" pra retornar a quantidade de trades ativos.
                # E aí comparar com o "setup.max_open_orders".
                # Não é o ideal fazer chamadas ao DB dentro do forloop, mas dado nosso contexto, me parece o correto mesmo. 
                # Até mais seguro do que ficar tentando tratarmos isso numa variável ou contador global.

                # TODO: Como previnir do robô entrar em mais de uma estratégia ao mesmo tempo?
                # Talvez mudar a logica do método manager.try_open_position pra retornar "true" caso a operação foi aberta?
                # Se foi aberta, então dar um comando para sair do forloop (talvez o "break"), e automaticamente ir para o próximo pair.  

                # Check if the strategy has been executed recently
                if not self.should_run_strategy(pair, strategy):
                    # Jump to the next strategy for this pair.
                    continue

                # Updates the last run time
                self.last_executions[(pair, strategy)] = datetime.now()
                final_dataset = self.create_combined_dataset(pair, strategy)

                #logging for debugging
                logger.info(f"TRYING TO OPEN POSITION - Pair: {pair}")
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

        opened_trades = trade_dao.get_open_trade_pairs()

        # TODO: What if an exception occurs in a specific trade?
        # We might want to continue processing the for loop and try to close the next trade. 
        for trade in opened_trades:
            strategyObject = strategy_dao.get_strategy_by_id(trade.strategy_id)
            strategyClassName = globals().get(strategyObject.name)
            #instantiate the strategy class:
            strategy = strategyClassName()

            # Check if the strategy has been opened in the last candle
            if not self.should_run_strategy(trade.pair, strategy):
                # Jump to the next opened trade.
                continue

            final_dataset = self.create_combined_dataset(trade.pair, strategy)

            #logging for debugging
            logger.info(f"TRYING TO CLOSE POSITION - Pair: {trade.pair}")
            logger.debug(f"Pair: {trade.pair} - datetime: {datetime.now()} - final_dataset:\n{final_dataset}")

            manager = StrategyManager(
                trade.pair,
                final_dataset,
                self.exchange_session.e_id,
                self.exchange_session.e_sk,
                self.setup.order_value,
                strategy
            )
            manager.try_close_position(strategy, trade.id)


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
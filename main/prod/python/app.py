from collections import OrderedDict
from common.python import database_operations as db
from noshirt import NoShirt
from env_setup import Env_setup
from ohcl import Ohcl
from common.python.strategy import *
from prod.python.login import Login
from backtesting.lib import resample_apply
import pandas_ta as ta
import pandas as pd

#todo calculate logic to get start date to ohcl_df (get now - biggest interval for trend indicators times strategy candle interval)
class Main():
    def __init__(self):
        base_config = db.get_initial_config()
        self.setup = Env_setup(base_config["max_open_orders"], base_config["order_value"], base_config["max_risk"], base_config["opperating"])
        self.exchange_session = Login("binance")
        self.exchange_session.login_database()
        self.strategies = [Strategy_B1()]

    # def initialize_dataset(self):
        # pass
    
    def run(self):
        while true:
            # Handle opened trades. Check if we is ready to sell.
            self.handleOpenedTrades()
        
            # Handle new positions to open.
            self.handleNewTrades()

    def handleNewTrades(self):
        # Check if the bot is in the state to open the position. 
        # If not then just do an early return, which means to skip the logic and do not run anything.
        is_bot_active = self.setup.opperating
        if not is_bot_active:
            return

        self.active_pairs = db.get_active_pairs()
        #deal with alerts here

        # Elegible Pairs means: pairs that are active and do not have any active alert).
        self.pairs = [pair for pair in self.active_pairs if pair not in db.get_open_orders()]

        for pair in self.pairs:
            for strategy in self.strategies:
                # self.run_control = {'pair': 'BTCUSDT', 'lastrun' : 'horario', 'period': '1h'}
                start_date = management.calc_start_date(strategy)
                #igualar datas de inicio
                intraday_candle_df = Ohcl(pair, strategy.intraday_interval, start_date)
                intraday_candle_df.populate_ohlc()

                trend_candle_df = Ohcl(pair, strategy.trend_interval, start_date)
                trend_candle_df.populate_ohlc()
                
                manager = NoShirt(pair, intraday_candle_df.ohcl_df, trend_candle_df.ohcl_df, self.exchange_session.e_id, self.exchange_session.e_sk, self.setup.order_value, strategy)
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

Main().run()


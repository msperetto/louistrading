import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from common import management
from common import database_operations as db
from backtest import NoShirt
from common.strategy import *
from prod.binance import Binance as binance
from enum import Enum
from backtest.python import Json_type
from itertools import product

# Useful constants
CASH = 150_000
COMISSION = 0.0015

class Main():
    def __init__(self):

        # Main config to run the Backtest:
        self.config = {
            "json_type": Json_type.INTRADAY,
            "should_save_report": True,
            "strategy_optimizer_mode": False,
            "should_plot_chart": False,
            "should_generate_CSV_trades": False,
            "should_run_portfolio_strategies": False
        }

        # Paths for JSONs
        self.json_paths = {
            Json_type.INTRADAY: "backtest/resources/intraday_params.json",
            Json_type.TREND: "backtest/resources/trend_params.json",
            Json_type.STRATEGY: "backtest/resources/strategy_params.json"
        }

        # Prepare to generate output files.
        self.path_plot = "backtest/output/plot/"
        self.path_csv = "backtest/output/csv/"

        # Inicializinzg some vars
        self.pair = None
        self.interval = None
        self.trend_interval = None

    # Runs the logic to save a row in the Optimization_test table.
    # It will save only if the global "should_save_report" flag is True.
    def save_report(self, stats):
        if self.config["should_save_report"]:
            cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
            db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label, self.trend_interval)

    def set_common_variables(self):
        # Load the JSON based on the configured json_type 
        json_path = self.json_paths[self.config["json_type"]]
        strategy_info = management.readJson(json_path)

        if not strategy_info:
            raise ValueError(f"The JSON defined in {json_path} is empty or invalid.")

        self.pair = strategy_info["pair"]
        self.intraday_interval = strategy_info["intraday_period"]
        self.trend_interval = strategy_info["trend_period"]
        self.period_label = strategy_info["period_label"]
        self.startTime = strategy_info["startTime"]
        self.endTime = strategy_info["endTime"]
        self.filter_buy_classes = strategy_info["filter_buy_classes"]
        self.trigger_buy_classes = strategy_info["trigger_buy_classes"]
        self.trade_buy_classes = strategy_info["trade_buy_classes"] 
        self.filter_sell_classes = strategy_info["filter_sell_classes"]
        self.trigger_sell_classes = strategy_info["trigger_sell_classes"]
        self.trade_sell_classes = strategy_info["trade_sell_classes"]
        self.trend_classes = strategy_info["trend_classes"]
        self.strategy_classes = strategy_info["strategy_classes"]

    def get_optimization_params(self):
        return {
            "sma_p_short": range(3, 4, 1),
            "sma_p_medium": range(15, 16, 1),
            "sma_p_long": range(50, 51, 1),
            "ema_p_short": range(8, 9, 1),
            "rsi_layer_cheap": range(22, 23, 1),
            "rsi_layer_expensive": range(79, 80, 1),
            "rsi_period": range(4, 5, 1),
            "max_candles_buy": range(5, 6, 1),
            "max_candles_sell": range(5, 6, 1),
            "intraday_interval": self.intraday_interval,
            "trend_interval": self.trend_interval
        }

    def run_intraday_optimization(self, bt):
        combinations = product(
            self.filter_buy_classes,
            self.trigger_buy_classes,
            self.trade_buy_classes,
            self.filter_sell_classes,
            self.trigger_sell_classes,
            self.trade_sell_classes
        )

        for combination in combinations:
            filter_buy_class, trigger_buy_class, trade_buy_class, filter_sell_class, trigger_sell_class, trade_sell_class = combination
            stats, heatmap = bt.optimize(
                **self.get_optimization_params(),
                filter_buy_class=db.get_class_code(filter_buy_class),
                trigger_buy_class=db.get_class_code(trigger_buy_class),
                trade_buy_class=db.get_class_code(trade_buy_class),
                filter_sell_class=db.get_class_code(filter_sell_class),
                trigger_sell_class=db.get_class_code(trigger_sell_class),
                trade_sell_class=db.get_class_code(trade_sell_class),
                maximize='Equity Final [$]',
                return_heatmap=True
            )
            self.save_report(stats)

    # Basically the main method.
    def start(self):
        self.set_common_variables()

        dataset = binance().get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)
        # TODO: Instead of NoShirt, it should use StrategyManager class. 
        bt = Backtest(dataset, NoShirt, CASH, COMISSION)

        match self.config["json_type"]:
            case Json_type.INTRADAY:
                self.run_intraday_optimization(bt)
                return
            case Json_type.TREND:
                print("Otimização para tendência ainda não implementada.")
                return
            case Json_type.STRATEGY:
                print("Otimização para estratégia ainda não implementada.")
                return
            case _:
                # Json_type not defined
                return
        
            
if __name__ == "__main__":
    Main().start()
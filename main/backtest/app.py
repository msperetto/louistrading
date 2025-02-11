import pandas_ta as ta
import pandas as pd
from common import management
from common.dao import database_operations as db
from common.strategy import *
from backtest import Json_type
from backtest.backtest_manager_intraday import BacktestManagerIntraday
from backtesting import Backtest
from prod.binance import Binance as binance
from enum import Enum
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
            Json_type.INTRADAY: "main/backtest/resources/intraday_params.json",
            Json_type.TREND: "main/backtest/resources/trend_params.json",
            Json_type.STRATEGY: "main/backtest/resources/strategy_params.json"
        }

        # Prepare to generate output files.
        self.path_plot = "main/backtest/output/plot/"
        self.path_csv = "main/backtest/output/csv/"

        # TODO: Maybe move this to global Strategies catalog? (similar to what we have for indicators - see: indicators_catalog.py)
        self.strategy_dict = {
            "B1": Strategy_B1(optimize=False),
            "B2": Strategy_B2(optimize=False),
            "B3": Strategy_B3(optimize=False),
            "C1": Strategy_C1(optimize=False)
        }

        self.strategy_optimize_dict = {
            "B1": Strategy_B1(optimize=True),
            "B2": Strategy_B2(optimize=True),
            "B3": Strategy_B3(optimize=True),
            "C1": Strategy_C1(optimize=True)
        }

        # Inicializinzg some vars
        self.pair = None
        self.interval = None
        self.trend_interval = None

    # Runs the logic to save a row in the Optimization_test table.
    # It will save only if the global "should_save_report" flag is True.
    def save_report(self, stats, strategy_class = ""):
        if self.config["should_save_report"]:
            cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
            db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label, self.trend_interval, strategy_class)

    def set_common_variables(self):
        # Load the JSON based on the configured json_type 
        json_path = self.json_paths[self.config["json_type"]]
        strategy_info = management.readJson(json_path)

        if not strategy_info:
            raise ValueError(f"The JSON defined in {json_path} is empty or invalid.")

        self.pair = strategy_info.get("pair", None)
        self.interval = strategy_info.get("intraday_period", None)
        self.trend_interval = strategy_info.get("trend_period", None)
        self.period_label = strategy_info.get("period_label", None)
        self.startTime = strategy_info.get("startTime", None)
        self.endTime = strategy_info.get("endTime", None)
        self.filter_buy_classes = strategy_info.get("filter_buy_classes", None)
        self.trigger_buy_classes = strategy_info.get("trigger_buy_classes", None)
        self.trade_buy_classes = strategy_info.get("trade_buy_classes", None)
        self.filter_sell_classes = strategy_info.get("filter_sell_classes", None)
        self.trigger_sell_classes = strategy_info.get("trigger_sell_classes", None)
        self.trade_sell_classes = strategy_info.get("trade_sell_classes", None)
        self.trend_classes = strategy_info.get("trend_classes", None)
        self.intraday_strategy_classes = strategy_info.get("intraday_strategy_classes", None)
        self.strategy_classes = strategy_info.get("strategy_classes", None)

    def get_optimization_params(self):
        return {
            "intraday_sma_short": range(3, 4, 1),
            "intraday_sma_medium": range(15, 16, 1),
            "intraday_sma_long": range(50, 51, 1),
            "intraday_ema_short": range(8, 9, 1),
            "intraday_rsi_layer_cheap": range(22, 23, 1),
            "intraday_rsi_layer_expensive": range(79, 80, 1),
            "intraday_rsi": range(4, 5, 1),
            "intraday_max_candles_buy": range(5, 6, 1),
            "intraday_max_candles_sell": range(5, 6, 1),
            "intraday_interval": self.interval,
            "trend_interval": self.trend_interval
        }

    def get_filename(self, strategy):
        return self.period_label+"-"+self.pair+"-"+self.interval+"-"+self.trend_interval+"-"+strategy

    def generate_CSV_trades(self, stats, strategy, trend_class = ""):
        if self.config["should_generate_CSV_trades"]:
            filename = self.get_filename(strategy)+"-"
            csv_trade_filename =  f"{self.path_csv+filename+trend_class}.csv"
            stats["_trades"].to_csv(csv_trade_filename)

    def plot_chart(self, bt, strategy, trend_class = ""):
        if self.config["should_plot_chart"]:
            filename = self.get_filename(strategy)+"-"
            bt.plot(filename=self.path_plot+filename+trend_class)

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
                filter_buy_class=filter_buy_class,
                trigger_buy_class=trigger_buy_class,
                trade_buy_class=trade_buy_class,
                filter_sell_class=filter_sell_class,
                trigger_sell_class=trigger_sell_class,
                trade_sell_class=trade_sell_class,
                maximize='Equity Final [$]',
                return_heatmap=True
            )
            self.save_report(stats)

    def get_strategy_class_name(self, strategy):
        return strategy.__class__.__name__

    def run_trend_strategy(self, bt, strategy):
        strategyName = self.get_strategy_class_name(strategy)
        for trend_class in self.trend_classes:
            stats = bt.run(**vars(strategy), trend_class=trend_class)
            self.save_report(stats, strategyName)
            self.generate_CSV_trades(stats, strategyName, trend_class)
            self.plot_chart(bt, strategyName, trend_class)

    def run_trend_strategy_optimization(self, bt, strategy):
        strategyName = self.get_strategy_class_name(strategy)
        for trend_class in self.trend_classes:
            stats, heatmap = bt.optimize(
                        **vars(strategy), 
                        trend_class=trend_class,
                        maximize = 'Equity Final [$]',
                        return_heatmap = True)

            self.save_report(stats, strategyName)

    def run_strategy(self, bt, strategy):
        if not hasattr(strategy, 'trend_class'):
            # Throw an exception in case strategy.trend_class is not defined.
            raise AttributeError("The strategy object does not have a 'trend_class' attribute.")

        # This method assumes the trend_class is defined inside of the strategy class.
        stats = bt.run(**vars(strategy))
        trend = strategy.trend_class

        strategyName = self.get_strategy_class_name(strategy)
        self.save_report(stats, strategyName)
        self.generate_CSV_trades(stats, strategyName, trend)
        self.plot_chart(bt, strategyName, trend)

    def run_strategy_optimization(self, bt, strategy):
        # This method assumes the trend_class is defined inside of the strategy class.
        stats, heatmap = bt.optimize(
                    **vars(strategy), 
                    maximize = 'Equity Final [$]',
                    return_heatmap = True)

        strategyName = self.get_strategy_class_name(strategy)
        self.save_report(stats, strategyName)

    # Basically the main method.
    def start(self):
        self.set_common_variables()

        dataset = binance().get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)
        bt = Backtest(dataset, BacktestManagerIntraday, cash=CASH, commission=COMISSION)

        match self.config["json_type"]:
            case Json_type.INTRADAY:
                self.run_intraday_optimization(bt)
                return
            case Json_type.TREND:
                # TODO: Define backtest using BacktestManagerStrategy.   
                # bt = Backtest(dataset, BacktestManagerStrategy, cash=CASH, commission=COMISSION)
                for strategy in self.intraday_strategy_classes:
                        method_name = self.run_trend_strategy_optimization if self.config["strategy_optimizer_mode"] else self.run_trend_strategy
                        strategy_param = self.strategy_optimize_dict[strategy] if self.config["strategy_optimizer_mode"] else self.strategy_dict[strategy]
                        method_name(bt, strategy_param)
                return
            case Json_type.STRATEGY:
                # The STRATEGY mode is used when we want to run backtest for many strategies.
                # About "should_run_portfolio_strategies":
                #   True: means that backtest will merge all the given strategies to act as a "single strategy". This is what we mean by Portfolio of Strategies. 
                #   False: means that backtest will run for each strategy individually.  
                if self.config["should_run_portfolio_strategies"]:
                    # TODO: Figure out how to run Backtest passing many strategies together. Use BacktestManagerPortfolio
                    pass
                else:
                    # This logic assumes the trend_class is defined inside of the strategy class.
                    for strategy in self.strategy_classes:
                        method_name = self.run_strategy_optimization if self.config["strategy_optimizer_mode"] else self.run_strategy
                        strategy_param = self.strategy_optimize_dict[strategy] if self.config["strategy_optimizer_mode"] else self.strategy_dict[strategy]
                        method_name(bt, strategy_param)                  
                return
            case _:
                # Json_type not defined
                return        
        
if __name__ == "__main__":
    print("Backtest started.")
    Main().start()
    print("Backtest finished.")
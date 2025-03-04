import pandas_ta as ta
import pandas as pd
from common import management
from common.dao import database_operations as db
from common.enums import Side_Type
from common.util import import_all_strategies
from common import STRATEGIES_PATH, STRATEGIES_MODULE
from backtest import Json_type
from backtest.backtest_manager_intraday import BacktestManagerIntraday
from backtest.backtest_manager_strategy import BacktestManagerStrategy
from backtest.backtest_manager_portfolio import BacktestManagerPortfolio
from backtesting import Backtest
from prod.binance import Binance as binance
from enum import Enum
from itertools import product
import math

# Useful constants
CASH = 150_000
COMISSION = 0.0015

def custom_score_optimization(stats):
    """Calcula um score baseado em Win Rate, número de Trades e Retorno Total."""
    win_rate = stats["Win Rate [%]"] / 100     # Convertendo para escala de 0 a 1
    num_trades = stats["# Trades"]
    total_return = stats["Return [%]"] / 100   # Convertendo para escala de 0 a 1

    if num_trades == 0:  # Evita erro de log(0)
        return 0

    return win_rate * math.log(num_trades) * total_return

class Main():
    def __init__(self):
        # Import all strategies from the strategies folder.
        import_all_strategies(STRATEGIES_PATH, STRATEGIES_MODULE, globals())

        # Main config to run the Backtest:
        self.config = {
            "json_type": Json_type.PORTFOLIO,
            "operation_type": Side_Type.SHORT,
            "should_save_report": True,
            "strategy_optimizer_mode": False,
            "should_plot_chart": False,
            "should_generate_CSV_trades": False,
            "should_run_portfolio_strategies": False
        }

        # Paths for JSONs
        self.json_paths = {
            Json_type.INTRADAY: "main/backtest/resources/intraday_params.json",
            Json_type.STRATEGY: "main/backtest/resources/strategy_params.json",
            Json_type.PORTFOLIO: "main/backtest/resources/portfolio_params.json"
        }

        # Prepare to generate output files.
        self.path_plot = "main/backtest/output/plot/"
        self.path_csv = "main/backtest/output/csv/"

        # Check if the trend should be automatically included in the strategy.
        self.shouldIncludeTrend = self.config["json_type"] == Json_type.PORTFOLIO
        self.optimize = self.config["strategy_optimizer_mode"]

        self.strategy_dict = self.create_strategy_dict([
            "B1", "B2", "S1", "S6", "S7",
            "SH1", "SH2", "SH3", "SH4", "SH5", "SH6", "SH7", "SH8", "SH9",
            "SC1", "SC1A", "SC1B", "SC1C", "SC2", "SC3", "SC4", "SC5", "SC6", "SC6A", "SC6B", "SC6C"
        ])

        # Inicializinzg some vars
        self.pair = None
        self.interval = None
        self.trend_interval = None


    def create_strategy_dict(self, strategy_keys):
        """Cria um dicionário de estratégias dinamicamente."""
        strategy_dict = {}
        for key in strategy_keys:
            strategy_class = globals().get(f"Strategy_{key}")  # Obtém a classe pelo nome
            if strategy_class:
                strategy_dict[key] = strategy_class(optimize=self.optimize, shouldIncludeTrend=self.shouldIncludeTrend)
            else:
                print(f"Warning: Class Strategy_{key} not found!")  # Mensagem opcional de debug
        return strategy_dict

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
            # "intraday_ema_short": 6,
            # "intraday_sma_medium": 19,
            # "intraday_sma_long": 50,
            # "intraday_rsi_layer_cheap": 22,
            # "intraday_rsi_layer_expensive": 80,
            # "intraday_rsi": 4,
            "intraday_ema_short": range(6, 10, 1),
            "intraday_sma_medium": range(17, 22, 1),
            "intraday_sma_long": range(48, 52, 1),
            "intraday_rsi_layer_cheap": 22,
            "intraday_rsi_layer_expensive": range(75, 86, 1),
            "intraday_rsi": range(3, 7, 1),
            # "intraday_max_candles_buy": range(5, 6, 1),
            # "intraday_max_candles_sell": range(5, 6, 1),
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
                operation_type=self.config["operation_type"],
                # maximize='Equity Final [$]',
                maximize = custom_score_optimization,
                return_heatmap=True
            )
            self.save_report(stats)

    def get_strategy_class_name(self, strategy):
        return strategy.__class__.__name__

    def run_trend_strategy(self, bt, strategy):
        strategyName = self.get_strategy_class_name(strategy)
        for trend_class in self.trend_classes:
            stats = bt.run(**vars(strategy), trend_class=trend_class, strategy_class=strategyName, operation_type=self.config["operation_type"])
            self.save_report(stats, strategyName)
            self.generate_CSV_trades(stats, strategyName, trend_class)
            self.plot_chart(bt, strategyName, trend_class)

    def run_trend_strategy_optimization(self, bt, strategy):
        strategyName = self.get_strategy_class_name(strategy)
        for trend_class in self.trend_classes:
            stats, heatmap = bt.optimize(
                        **vars(strategy), 
                        trend_class=trend_class,
                        strategy_class=strategyName,
                        operation_type=self.config["operation_type"],
                        # maximize = 'Equity Final [$]',
                        # maximize = 'Win Rate [%]',
                        maximize = custom_score_optimization,
                        return_heatmap = True)

            self.save_report(stats, strategyName)

    def run_strategy(self, bt, strategy):
        strategyName = self.get_strategy_class_name(strategy)

        if not hasattr(strategy, 'trend_class'):
            # Throw an exception in case strategy.trend_class is not defined.
            message = f"The strategy {strategyName} object does not have a 'trend_class' attribute."
            raise AttributeError(message)

        # This method assumes the trend_class is defined inside of the strategy class.
        stats = bt.run(**vars(strategy), strategy_class=strategyName, operation_type=self.config["operation_type"])
        trend = strategy.trend_class

        self.save_report(stats, strategyName)
        self.generate_CSV_trades(stats, strategyName, trend)
        self.plot_chart(bt, strategyName, trend)

    def run_strategy_optimization(self, bt, strategy):
        # This method assumes the trend_class is defined inside of the strategy class.
        strategyName = self.get_strategy_class_name(strategy)
        stats, heatmap = bt.optimize(
                    **vars(strategy), 
                    strategy_class=strategyName,
                    operation_type=self.config["operation_type"],
                    # maximize = 'Equity Final [$]',
                    maximize = custom_score_optimization,
                    return_heatmap = True)

        self.save_report(stats, strategyName)

    def get_backtest_manager(self):
        match self.config["json_type"]:
            case Json_type.INTRADAY:
                return BacktestManagerIntraday
            case Json_type.STRATEGY:
                return BacktestManagerStrategy
            case Json_type.PORTFOLIO:
                return BacktestManagerPortfolio

    # Basically the main method.
    def start(self):
        self.set_common_variables()

        dataset = binance().get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)
        bt = Backtest(dataset, self.get_backtest_manager(), cash=CASH, commission=COMISSION)

        match self.config["json_type"]:
            case Json_type.INTRADAY:
                self.run_intraday_optimization(bt)
                return
            case Json_type.STRATEGY:
                # TODO: Define backtest using BacktestManagerStrategy.   
                # bt = Backtest(dataset, BacktestManagerStrategy, cash=CASH, commission=COMISSION)
                for strategy in self.intraday_strategy_classes:
                        method_name = self.run_trend_strategy_optimization if self.config["strategy_optimizer_mode"] else self.run_trend_strategy
                        strategy_param = self.strategy_dict[strategy]
                        method_name(bt, strategy_param)
                return
            case Json_type.PORTFOLIO:
                # The PORTFOLIO mode is used when we want to run backtest for many strategies.
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
                        strategy_param = self.strategy_dict[strategy]
                        method_name(bt, strategy_param)                  
                return
            case _:
                # Json_type not defined
                return        
        
if __name__ == "__main__":
    print("Backtest started.")
    Main().start()
    print("Backtest finished.")
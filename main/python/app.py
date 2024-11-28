import pandas_ta as ta
import pandas as pd
import binance 
import management
import database_operations as db
from backtest import PlaygroundLouis, NoShirt
from backtesting import Backtest
from strategy import *


class Main():
    def __init__(self):
        strategy_info = management.readJson("main/resources/params.json")
        self.pair = strategy_info["pair"]
        self.interval = strategy_info["period"]
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

        self.strategy_dict = {
            "B1": Strategy_B1(optimize=False),
            "B2": Strategy_B2(optimize=False),
            "B3": Strategy_B3(optimize=False),
            "B4": Strategy_B4(optimize=False),
            "B5": Strategy_B5(optimize=False),            
            "C1": Strategy_C1(optimize=False),
            "X1": Strategy_X1(optimize=False),
            "X2": Strategy_X2(optimize=False),
            "X3": Strategy_X3(optimize=False)
        }
        self.strategy_optimize_dict = {
            "B1": Strategy_B1(),
            "B2": Strategy_B2(),
            "B3": Strategy_B3(),
            "B4": Strategy_B4(),
            "B5": Strategy_B5(),
            "C1": Strategy_C1(),
            "X1": Strategy_X1(),
            "X2": Strategy_X2(),
            "X3": Strategy_X3()
        }

    def plot_single_strat(self, bt, filename, strategy, trend_class="UpTrend_AlwaysTrend", should_plot = True):
        stats = bt.run(**vars(strategy), trend_class=db.get_class_code(trend_class))

        cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
        db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label, self.trend_interval, strategy.__class__.__name__)

        trades_filename = f"main/outputs/{filename+trend_class}.csv"

        stats["_trades"].to_csv(trades_filename)

        if should_plot: bt.plot(filename=filename+trend_class)

    def run_optimization(self, bt):
        for filter_buy_class in self.filter_buy_classes:
            for trigger_buy_class in self.trigger_buy_classes:
                for trade_buy_class in self.trade_buy_classes:
                    for filter_sell_class in self.filter_sell_classes:
                        for trigger_sell_class in self.trigger_sell_classes:
                            for trade_sell_class in self.trade_sell_classes:
                                stats, heatmap = bt.optimize(
                                            sma_p_short = range(3,4,1),
                                            sma_p_medium = range(15,16,1),
                                            sma_p_long = range(50,51,1),
                                            ema_p_short = range(8,9,1),
                                            rsi_layer_cheap = range(22, 23, 1),
                                            rsi_layer_expensive = range(79, 80, 1),
                                            rsi_period = range(4, 5, 1),
                                            max_candles_buy = range(5, 6, 1),
                                            max_candles_sell = range(5, 6, 1),
                                            trend_interval = self.trend_interval,
                                            # stop_loss = range(2,5,1), # percentage of maximum loss - float number (i.e. 3 or 2.5 etc)
                                            # take_profit = range() # percentage of maximum profit - float number
                                            filter_buy_class=db.get_class_code(filter_buy_class),
                                            trigger_buy_class=db.get_class_code(trigger_buy_class),
                                            trade_buy_class=db.get_class_code(trade_buy_class),
                                            filter_sell_class=db.get_class_code(filter_sell_class),
                                            trigger_sell_class=db.get_class_code(trigger_sell_class),
                                            trade_sell_class=db.get_class_code(trade_sell_class),
                                            maximize = 'Equity Final [$]',
                                            return_heatmap = True)

                                cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
                                db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label, self.trend_interval)

    
    def run_trend_strat(self, bt, filename, strategy, trend_class="UpTrend_AlwaysTrend", should_plot = True):
        for trend_class in self.trend_classes:
            stats = bt.run(**vars(strategy), trend_class=db.get_class_code(trend_class))

            cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
            db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label, self.trend_interval, strategy.__class__.__name__)

            trades_filename = f"main/outputs/{filename+trend_class}.csv"
            stats["_trades"].to_csv(trades_filename)

            if should_plot: bt.plot(filename=filename+trend_class)


    def run_trend_optimization(self, bt, strategy):
        for trend_class in self.trend_classes:
            stats, heatmap = bt.optimize(
                        **vars(strategy), 
                        trend_class=db.get_class_code(trend_class),
                        maximize = 'Equity Final [$]',
                        return_heatmap = True) 

            cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
            db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label, self.trend_interval, strategy.__class__.__name__)


    def run_backtest(self):

        dataset = binance.get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)
        bt = Backtest(dataset, NoShirt, cash=150_000, commission=0.0015)

        # self.run_optimization(bt)

        for strategy in self.strategy_classes:
            filename = self.period_label+"-"+self.pair+"-"+self.interval+"-"+self.trend_interval+"-"+strategy+"-"
            
            # self.run_trend_optimization(bt, self.strategy_optimize_dict[strategy])
            # self.plot_single_strat(bt, filename, self.strategy_dict[strategy])
            self.run_trend_strat(bt, filename, self.strategy_dict[strategy], "UpTrend_EMAshort_gt_SMAlong", True)

          
Main().run_backtest()

# df.ta.rsi(length=40, append=True)
# help(df.ta.indicators())
# help(ta.sma)
# print(df.dtypes)




# metamask: aevo
# Register

#     Key:
#     0xe0176e52e4ae6ffaa8d8a815d9a25f84545be455ddbb1a717934ed4f4276d325
#     Expiry:
#     1713539274
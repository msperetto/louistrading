import pandas_ta as ta
import pandas as pd
import binance 
import management
import database_operations as db
from backtest import PlaygroundLouis
from backtesting import Backtest


class Main():
    def __init__(self):
        strategy_info = management.readJson("main/resources/params.json")
        self.pair = strategy_info["pair"]
        self.interval = strategy_info["period"]
        self.period_label = strategy_info["period_label"]
        self.startTime = strategy_info["startTime"]
        self.endTime = strategy_info["endTime"]
        self.filter_buy_classes = strategy_info["filter_buy_classes"]
        self.trigger_buy_classes = strategy_info["trigger_buy_classes"]
        self.trade_buy_classes = strategy_info["trade_buy_classes"] 
        self.filter_sell_classes = strategy_info["filter_sell_classes"]
        self.trigger_sell_classes = strategy_info["trigger_sell_classes"]
        self.trade_sell_classes = strategy_info["trade_sell_classes"]
 
        # self.strategies = [strategy["indicator"] for strategy in strategy_info["strategy"]]
        # self.params = [strategy["params"] for strategy in strategy_info["strategy"]]

    def run_strategies(self):
        previous_interval = 0
        df_list = []
        for index, interval in enumerate(self.interval):
            strategy_params = management.dict_to_params(self.params[index])
            if previous_interval != interval:
                df_list.append(binance.get_kline(self.pair, interval, self.startTime))
                exec(f"df_list[{index}].ta.{self.strategies[index]}({strategy_params}, append=True)")
            previous_interval = interval
            # todo execute ta strategy if same interval

        for df in df_list:
            print(df)


    def run_backtest(self):

        dataset = binance.get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)
        dataset2 = binance.get_extended_kline(self.pair, self.interval, self.startTime, self.endTime)
        bt = Backtest(dataset, PlaygroundLouis, cash=150_000, commission=0.0015)

        for filter_buy_class in self.filter_buy_classes:
            for trigger_buy_class in self.trigger_buy_classes:
                for trade_buy_class in self.trade_buy_classes:
                    for filter_sell_class in self.filter_sell_classes:
                        for trigger_sell_class in self.trigger_sell_classes:
                            for trade_sell_class in self.trade_sell_classes:
                                stats, heatmap = bt.optimize(
                                            # sma_p_short = range(3,4,1),
                                            # sma_p_medium = range(15,16,1),
                                            sma_p_long = range(50,51,1),
                                            ema_p_short = range(8,10,1),
                                            rsi_layer_cheap = range(22, 23, 1),
                                            rsi_layer_expensive = range(78, 80, 1),
                                            rsi_period = range(4, 7, 1),
                                            max_candles_buy = range(5, 7, 1),
                                            max_candles_sell = range(5, 7, 1),
                                            stop_loss = range(2,5,1), # percentage of maximum loss - float number (i.e. 3 or 2.5 etc)
                                            # take_profit = range() # percentage of maximum profit - float number
                                            filter_buy_class=db.get_class_code(filter_buy_class),
                                            trigger_buy_class=db.get_class_code(trigger_buy_class),
                                            trade_buy_class=db.get_class_code(trade_buy_class),
                                            filter_sell_class=db.get_class_code(filter_sell_class),
                                            trigger_sell_class=db.get_class_code(trigger_sell_class),
                                            trade_sell_class=db.get_class_code(trade_sell_class),
                                            maximize = 'Equity Final [$]',
                                            return_heatmap = True)
                                        
                                        # print(heatmap.sort_values().iloc[-7:])
                                            

                                # stats = bt.run(
                                #     sma_p_short=2,
                                #     sma_p_medium=15,
                                #     sma_p_long=52,
                                #     ema_p_short=5,
                                #     rsi_period=4,
                                #     rsi_layer_cheap=23,
                                #     rsi_layer_expensive=73,
                                #     max_candles=6,
                                #     filter_buy_class=filter_buy_class,
                                #     trigger_buy_class=trigger_buy_class,
                                #     trade_buy_class=trade_buy_class,
                                #     filter_sell_class=filter_sell_class,
                                #     trigger_sell_class=trigger_sell_class,
                                #     trade_sell_class=trade_sell_class)

                                cut_long_string = str(stats["_strategy"]).find(",filter_buy_class")
                                db.insert_report(self.pair, str(self.interval), stats, str(stats["_strategy"])[:cut_long_string]+")", self.period_label)
           
        # bt.plot()
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
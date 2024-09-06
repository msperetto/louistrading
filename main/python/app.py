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
        self.interval = [interval["period"] for interval in strategy_info["strategy"]]
        self.strategies = [strategy["indicator"] for strategy in strategy_info["strategy"]]
        self.params = [strategy["params"] for strategy in strategy_info["strategy"]]
        self.startTime = strategy_info["startTime"]
        

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
        dataset = binance.get_extended_kline(self.pair, self.interval[0], self.startTime)
        bt = Backtest(dataset, PlaygroundLouis, cash=150_000, commission=0.0015)

        stats = bt.run(
            sma_period_medium=15,
            sma_period_long=48,
            rsi_period=5,
            rsi_layer_cheap=26,
            rsi_layer_expensive=80,
            max_candles=5)
            
            # filter = FilterBuy_RSI(self.rsi, self.rsi_layer_cheap),
            # triggeredState = TriggeredState_MaxCandles(5, False),
            # trade = Trade_Buy_HighLastCandle())


        # stats, heatmap = bt.optimize(
        #     rsi_layer_cheap = range(19, 23, 1),
        #     rsi_layer_expensive = range(80, 85, 1),
        #     rsi_period = range(4, 7, 1),
        #     # sma_period_medium = range(15, 20, 1),
        #     # sma_period_long = range(45, 50, 1),
        #     max_candles = range(4, 5, 1),
        #     maximize = 'Equity Final [$]',
        #     return_heatmap = True)
        
        print(stats)
        # db.insert_report(self.pair, 'Name_RSI', stats, str(stats["_strategy"]))
        # print(heatmap.sort_values().iloc[-7:])
             
        bt.plot()
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
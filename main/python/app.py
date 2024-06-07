import pandas_ta as ta
import pandas as pd
import binance 
import management
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
        dataset = binance.get_kline(self.pair, self.interval[0], self.startTime)
        bt = Backtest(dataset, PlaygroundLouis, cash=1_000_000, commission=0.0015)
        print(bt.run(sma_period1=21, sma_period2=50, rsi_period=3, rsi_layer1=20, rsi_layer2=80))
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
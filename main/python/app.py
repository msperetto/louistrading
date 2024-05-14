import pandas_ta as ta
import pandas as pd
import binance
import management

def run_strategies():
    strategy_info = management.readJson("main/resources/params.json")

    pair = strategy_info["pair"]
    interval = [interval["period"] for interval in strategy_info["strategy"]]
    strategies = [strategy["indicator"] for strategy in strategy_info["strategy"]]
    params = [strategy["params"] for strategy in strategy_info["strategy"]]
    startTime = strategy_info["startTime"]

    previous_interval = 0
    df_list = []
    for index, interval in enumerate(interval):
        strategy_params = management.dict_to_params(params[index])
        if previous_interval != interval:
            df_list.append(binance.get_kline(pair, interval, startTime))
            exec(f"df_list[{index}].ta.{strategies[index]}({strategy_params}, append=True)")
        previous_interval = interval

    for df in df_list:
        print(df)


run_strategies()

# df.ta.sma(length=20, append=True)
# df.ta.ema(length=20, append=True)
# df.ta.rsi(length=40, append=True)
# help(df.ta.indicators())
# help(ta.sma)
# print(df.dtypes)


# print(df)

# metamask: aevo
# Register

#     Key:
#     0xe0176e52e4ae6ffaa8d8a815d9a25f84545be455ddbb1a717934ed4f4276d325
#     Expiry:
#     1713539274
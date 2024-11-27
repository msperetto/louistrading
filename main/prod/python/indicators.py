import pandas_ta as ta
from dataset import Dataset as ohlc_df

class Indicators():
    def __init__(self):
        #initializing strategy (group of indicators)
        self.strategy = ta.Strategy(
            name="grouping_indicators",
            ta=[{}]
        )

    def calc_indicator(self, df: ohlc_df, indicator: str, **kwargs):
        try:
            return df.ta(kind=indicator, append=True, **kwargs)
        except Exception as e:
            raise RuntimeError(f'Indicator "{indicator}" error with exception: {e}')

    def add_indicator_to_strategy(self, indicator):
        #indicator has to be a dictionary like: {"kind": "rsi", "length": 22}
        self.strategy.ta.append(indicator)

    def apply_strategy_to_df(self, df):
        df.ta.strategy(self.strategy)

    def join_indicator_to_dataset(self, df, indicator):
        return df.join(indicator)




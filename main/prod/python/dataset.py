import pandas_ta as ta
from common.python.indicators_catalog import indicators_catalog

class Dataset():
    def __init__(self):
        #initializing strategy (group of indicators)
        #a strategy for pandas_ta is a group of indicators that will be added to the dataset
        self.strategy = ta.Strategy(
            name="grouping_indicators",
            ta=[{}]
        )

    def calc_indicator(self, df, indicator: str, **kwargs):
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

    # add the indicators columns to the candles dataset
    def add_indicators_to_candle_dataset(self, dataset, strategy, period_type):
        indicator_df = Dataset()
        indicator_df.strategy.ta.remove({})
        indicators_list = []

        for attr, config in indicators_catalog.items():
            if config['period_type'] == period_type:
                try:
                    indicators_list.append({"kind": config['prefix'], "length": getattr(strategy, attr)})
                except AttributeError:
                    pass

        for indicator in indicators_list:
            indicator_df.add_indicator_to_strategy(indicator)
            
        #here the dataset will be updated
        indicator_df.apply_strategy_to_df(dataset)

        return [indicator['kind'].upper()+'_'+str(indicator['length']) for indicator in indicators_list]


    def merge_dataframes(intraday_df, trend_df, *trend_indicators):
        intraday_df['date'] = intraday_df.index.date
        trend_df['date'] = trend_df.index.date

        df_merged = pd.merge(
            intraday_candle_df.ohcl_df,
            trend_candle_df.ohcl_df[list(trend_indicators)],
            on='date',
            how='left'
        )

        df_merged.set_index(intraday_df.index, inplace=True)

        df_merged.drop(columns=['date'], inplace=True)

        return df_merged




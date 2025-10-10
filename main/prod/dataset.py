import talib
import pandas as pd
import numpy as np
from common.indicators_catalog import indicators_catalog

class Dataset():
    def __init__(self, dataset, strategy):
        self.dataset = dataset
        self.strategy = strategy
        self.indicator_management = []

    def calc_indicator(self, indicator: str, **kwargs):
        try:
            # Map pandas_ta indicators to talib equivalents
            indicator_map = {
                'ema': talib.EMA,
                'sma': talib.SMA,
                'rsi': talib.RSI,
                'adx': talib.ADX
            }
            
            if indicator.lower() not in indicator_map:
                raise ValueError(f'Indicator "{indicator}" not supported')
            
            talib_func = indicator_map[indicator.lower()]
            length = kwargs.get('length', 14)
            
            # Get the appropriate price data based on indicator
            if indicator.lower() == 'adx':
                high = self.dataset['High'].values if 'High' in self.dataset.columns else self.dataset['high'].values
                low = self.dataset['Low'].values if 'Low' in self.dataset.columns else self.dataset['low'].values
                close = self.dataset['Close'].values if 'Close' in self.dataset.columns else self.dataset['close'].values
                result = talib_func(high, low, close, timeperiod=length)
            else:
                close = self.dataset['Close'].values if 'Close' in self.dataset.columns else self.dataset['close'].values
                result = talib_func(close, timeperiod=length)
            
            # Convert to pandas Series and add to dataset
            result_series = pd.Series(result, index=self.dataset.index)
            result_series.name = f'{indicator.upper()}_{length}'
            self.dataset[result_series.name] = result_series
            return result_series
            
        except Exception as e:
            raise RuntimeError(f'Indicator "{indicator}" error with exception: {e}')

    def add_indicator_to_manager(self, indicator):
        #indicator has to be a dictionary like: {"kind": "rsi", "length": 22}
        self.indicator_management.append(indicator)

    def apply_indicators_to_df(self):
        for indicator in self.indicator_management:
            self.calc_indicator(indicator['kind'], length=indicator['length'])

    def join_indicator_to_dataset(self, indicator):
        return self.dataset.join(indicator)

    # add the indicators columns to the candles dataset
    def add_indicators_to_candle_dataset(self, period_type):
        self.indicator_management = []
        indicators_list = []

        for attr, config in indicators_catalog.items():
            if config['period_type'] == period_type:
                try:
                    indicators_list.append({"kind": config['prefix'], "length": getattr(self.strategy, attr)})
                    if period_type == 'trend':
                        indicators_list[-1]['prefix'] = 'TREND'
                except AttributeError:
                    pass

        for indicator in indicators_list:
            self.add_indicator_to_manager(indicator)
            
        #here the dataset will be updated
        self.apply_indicators_to_df()

        # when trend dataset, return a list of the column names to be merged later
        # TODO: maybe later create a method only for that
        if period_type == 'trend':
            return ['TREND_'+indicator['kind'].upper()+'_'+str(indicator['length']) for indicator in indicators_list]


    # method to merge only the indicators from one dataframe to other
    def merge_dataframes(self, df_to_merge, *to_merge_indicators):
        self.dataset['date'] = self.dataset.index.date
        df_to_merge['date'] = df_to_merge.index.date
        
        # adding calculated column 'date' to the indicators to merge
        indicators_to_merge = list(to_merge_indicators)
        indicators_to_merge.append('date')

        df_merged = pd.merge(
            self.dataset,
            df_to_merge[list(indicators_to_merge)],
            on='date',
            how='left'
        )

        df_merged.set_index(self.dataset.index, inplace=True)

        df_merged.drop(columns=['date'], inplace=True)

        return df_merged




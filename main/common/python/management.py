from datetime import datetime
import json
import pandas as pd

def date_to_ms(date_value: str):
    date_value = datetime.strptime(date_value, '%d.%m.%Y')
    return int(date_value.timestamp() * 1000)

def readJson(file):
    with open(file, 'r') as f:
        return json.load(f)

def time_intervals_to_seconds(interval):
    interval_map = {
        "1h": 3600,
        "2h": 7200,
        "6h": 21600,
        "12h": 43200,
        "1d": 86400
    }
    return interval_map[interval]

def dict_to_params(dict):
    params = json.dumps(dict)
    params = params.replace(":","=")
    params = params.replace("{","")
    params = params.replace("}","")
    params = params.replace('"',"")
    return params

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
from datetime import datetime, timedelta
import json
import pandas as pd
from common.strategy import *

# number 5 is only to increase a bit the size of biggest indicator interval
# to have bigger margin for calculation
TREND_INTERVAL_CALC_MARGIN = 5

def date_to_ms(date_value):
    date_value = datetime.strptime(date_value, '%d.%m.%Y') if isinstance(date_value, str) else date_value
    return int(date_value.timestamp() * 1000)

def readJson(file):
    with open(file, 'r') as f:
        return json.load(f)

def time_intervals_to_seconds(interval):
    interval_map = {
        "1h": 3600,
        "2h": 7200,
        "4h": 14400,
        "6h": 21600,
        "8h": 28800,
        "12h": 43200,
        "1d": 86400,
        "D": 86400,
        "1D": 86400
    }
    return interval_map[interval]

def time_intervals_to_minutes(interval):
    interval_map = {
        "1h": 60,
        "2h": 120,
        "4h": 240,
        "8h": 480,
        "1d": 1440
    }
    return interval_map[interval]


def dict_to_params(dict):
    params = json.dumps(dict)
    params = params.replace(":","=")
    params = params.replace("{","")
    params = params.replace("}","")
    params = params.replace('"',"")
    return params

#calculate start date to get ohcl dataset, based on the biggest timeframe interval from strategy class
def calc_start_date(strategy = None, trend_period = None, longest_indicator = None, base_start_date = datetime.now()):
    if strategy:
        # calculating the total amount of time in seconds to be able to calculate the longest trend indicator
        diff_size = time_intervals_to_seconds(strategy.trend_interval)*(strategy.get_biggest_trend_interval()+TREND_INTERVAL_CALC_MARGIN)
        start_date = base_start_date - timedelta(seconds=diff_size)
        return start_date.strftime('%d.%m.%Y')
    
    if trend_period:
        # calculating the total amount of time in seconds to be able to calculate the longest trend indicator
        diff_size = time_intervals_to_seconds(trend_period)*(longest_indicator)
        start_date = base_start_date - timedelta(seconds=diff_size)
        return start_date

    raise ValueError("Either strategy or (trend_period and longest_indicator) must be provided to calculate start date.")


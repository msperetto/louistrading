from datetime import datetime, timedelta
import json
import pandas as pd
from common.strategy import *

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
def calc_start_date(strategy):
    # calculating the total amount of time in seconds to be able to calculate the longest trend indicator
    # number 5 is only to increase a bit the size to have bigger margin for calculation
    diff_size = time_intervals_to_seconds(strategy.trend_interval)*(strategy.trend_longest_indicator_value+5)
    start_date = datetime.now() - timedelta(seconds=diff_size)
    return start_date.strftime('%d.%m.%Y')


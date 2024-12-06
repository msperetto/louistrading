from datetime import datetime
import json

def date_to_ms(date_value: str):
    date_value = datetime.strptime(date_value, '%d.%m.%Y')
    return int(date_value.timestamp() * 1000)

def readJson(file):
    with open(file, 'r') as f:
        return json.load(f)

def time_intervals_to_seconds(interval):
    interval_map = {
        "h": 3600,
        "2h": 7200,
        "6h": 21600,
        "12h": 43200,
        "D": 86400
    }
    return interval_map[interval]

def dict_to_params(dict):
    params = json.dumps(dict)
    params = params.replace(":","=")
    params = params.replace("{","")
    params = params.replace("}","")
    params = params.replace('"',"")
    return params

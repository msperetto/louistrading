from datetime import datetime
import json

def date_to_ms(date_value: str):
    date_value = datetime.strptime(date_value, '%d.%m.%Y')
    return int(date_value.timestamp() * 1000)

def readJson(file):
    with open(file, 'r') as f:
        return json.load(f)

def dict_to_params(dict):
    params = json.dumps(dict)
    params = params.replace(":","=")
    params = params.replace("{","")
    params = params.replace("}","")
    params = params.replace('"',"")
    return params
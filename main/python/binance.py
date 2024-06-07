import pandas as pd
import management
import time
import asyncio
from typing import List, Dict
from urllib.parse import urlencode
import hashlib
import hmac
import sys
import configparser
import requests
# import aiohttp
from datetime import datetime
import json
# import websockets

BASE_ENDPOINT = 'https://fapi.binance.com'
WS_ENDPOINT = 'wss://fstream.binance.com/ws/'

def get_servertime():
    request_path = '/fapi/v1/time'
    binance_out = 1
    while binance_out:
        try:
            return requests.get(BASE_ENDPOINT + request_path).json()['serverTime']
        except requests.exceptions.SSLError:
            print(f'Max retries exceeded with url: /api/v3/time')
            time.sleep(4)
        except Exception as e:
            print(
                f'Binance trade server time out - sleeps 3 secs - {sys.exc_info()}')
            time.sleep(3)


def sign_request(params, b_id, b_sk):
    """given params create the signature to make any binance auth request

    Args:
        params (dict): params from any binance margin request

    Returns:
        (string): API ID of binance account
        (hmac): signature for binance request
    """
    # apagar comentarios abaixo
    # config_parser = configparser.ConfigParser()
    # config_parser.read("main/resources/data/config.ini")
    # b_key = bytes(config_parser["binance"]["segredo"], "utf-8")
    params_binance_sign = bytes(urlencode(params), 'utf-8')
    params['signature'] = hmac.new(
        b_sk, params_binance_sign, digestmod=hashlib.sha256).hexdigest()
    return b_id


def run_signed_request(path, params, type_req, b_id, b_sk):
    api_id = sign_request(params, b_id, b_sk)
    if type_req == 'get':
        binance_out = 1
        while binance_out:
            try:
                return requests.get(BASE_ENDPOINT + path, params=params,
                                    headers={"X-MBX-APIKEY": api_id}).json()
            except Exception as e:
                time.sleep(3)
                serverTime = get_servertime()
                params['timestamp'] = str(serverTime)
                params.pop('signature')
                sign_request(params, b_id, b_sk)
    else:
        binance_out = 1
        while binance_out:
            try:
                return requests.post(BASE_ENDPOINT + path, params=params,
                                     headers={"X-MBX-APIKEY": api_id}).json()
            except Exception as e:
                time.sleep(3)
                serverTime = get_servertime()
                params['timestamp'] = str(serverTime)
                params.pop('signature')
                sign_request(params, b_id, b_sk)


def get_all_symbols():
    endpoint = '/fapi/v1/exchangeInfo'
    binance_out = 1

    while binance_out:
        try:
            exchange_info = requests.get(
                BASE_ENDPOINT + endpoint).json()['symbols']
            binance_out = 0
        except Exception as e:
            time.sleep(1)

    result = [symbols['symbol'] for symbols in exchange_info if symbols['status'] == "TRADING"]

    
    return result


async def get_orderbook(pairs_to_filter: list[str], pair: str = None):
    endpoint = "/fapi/v1/ticker/bookTicker"

    binance_out = 1

    if pair:
        params = {
            "symbol": pair,
        }
    else:
        params = None

    while binance_out:
        try:
            async with aiohttp.ClientSession() as session:
                exchange_info = await session.get(BASE_ENDPOINT + endpoint, params=params, ssl=False)
                result = await exchange_info.json()
            binance_out = 0
        except Exception as e:
            print(e)
            time.sleep(1)
    
    # filtering results for only pairs in intersections between the two exchanges:
    filtered_result = [pair for pair in result if pair["symbol"] in pairs_to_filter]

    # ordering results based on symbol name:
    ordered_result = sorted(filtered_result, key=lambda i: i["symbol"])

    return ordered_result
    # return [float(result["bidPrice"]), float(result["askPrice"])]

def get_kline(pair: str, interval: str, startTime: str, endTime: int = round(time.time() * 1000)):
    endpoint = "/fapi/v1/klines"
    params = {
        "symbol": pair,
        "interval": interval,
        "startTime": management.date_to_ms(startTime),
        "endTime": endTime,
        "limit": 1500
    }

    try:
        kline = requests.get(
            BASE_ENDPOINT + endpoint, params=params).json()
        binance_out = 0
    except Exception as e:
        print(e)
    
    df = pd.DataFrame(kline, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Tbbav', 'Tbqav', 'Ignore'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.drop(['Close_time','Quote_asset_volume', 'Number_of_trades', 'Tbbav', 'Tbqav', 'Ignore'], axis=1, inplace=True)
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df.set_index('Date', inplace=True)
    return df

def get_bid(pair_info: dict):
    return pair_info["bidPrice"]


def get_ask(pair_info: dict):
    return pair_info["askPrice"]


# async def get_bid_ask(pair: str) -> list:
#     print(get_orderbook(pair))
#     bid = await get_orderbook(pair)["bidPrice"]
#     ask = await get_orderbook(pair)["askPrice"]
#     return await [bid, ask]


async def get_mark_funding():
    endpoint = '/fapi/v1/premiumIndex'

    binance_out = 1

    while binance_out:
        try:
            async with aiohttp.ClientSession() as session:
                exchange_info = await session.get(BASE_ENDPOINT + endpoint, ssl=False)
                result = await exchange_info.json()
            binance_out = 0
        except Exception as e:
            print(e)
            time.sleep(1)

    return result


def get_funding_rate_history(symbol, limit=100):
    endpoint = '/dapi/v1/fundingRate'
    params = {
        'symbol': symbol,
        'limit': limit
    }
    binance_out = 1
    funding_rates = []

    while binance_out:
        try:
            funding_rates = requests.get(
                BASE_ENDPOINT + endpoint, params=params).json()
            binance_out = 0
        except Exception as e:
            time.sleep(3)

    funding_rates = transformUnixTimeInDatetime(funding_rates, "fundingTime")
    funding_rates = transformStrToFloat(funding_rates, "fundingRate")

    return funding_rates


def transformUnixTimeInDatetime(entry_dict, field):
    for entry in entry_dict:
        entry[field] = str(datetime.fromtimestamp(int(entry[field]/1000)))
    return entry_dict


def transformStrToFloat(entry_dict, field):
    for entry in entry_dict:
        entry[field] = float(entry[field])
    return entry_dict


def open_position(symbol, amount, side, price, b_id, b_sk):
    endpoint = '/fapi/v1/order'

    params = {
        'symbol': symbol,
        'side': side, #"BUY" or "SELL"
        'type': 'LIMIT',
        'quantity': management.truncate(amount, 0),
        'price': management.truncate(price, 5),
        # IOC execute all quantity possible and cancel any remaining qtt;
        'timeInForce': 'IOC',
        'timestamp': str(get_servertime()),
        'recvWindow': 3000
    }
    print(f"qtt {management.truncate(amount, 0)}")
    print(f"price {management.truncate(price, 5)}")


    position = run_signed_request(endpoint, params, 'post', b_id, b_sk)
    if 'code' in position.keys(): # erro no servidor binance
        print(position)
        print(f'Tentativa arbitragem com erro na Binance')
    else:
        return position

def query_order(symbol, orderId, b_id, b_sk):
    endpoint = '/fapi/v1/order'

    params = {
        'symbol': symbol,
        'orderId': orderId,
        'recvWindow': 5000,
        'timestamp': str(get_servertime())
    }

    binance_out = 1
    while binance_out:
        order_info = run_signed_request(endpoint, params, 'get', b_id, b_sk)
        if 'code' in order_info.keys():
            print(f'erro query_order {order_info} coin: {symbol}')
        else:
            return order_info


def account_info(b_id, b_sk):
    endpoint = '/fapi/v2/account'

    params = {
        'timestamp': str(get_servertime())
    }
    return run_signed_request(endpoint, params, 'get', b_id, b_sk)

def get_bid_ask_from_ws(ws_response: str):
    return [ws_response["b"], ws_response["a"]]

async def ws_get_orderbook_stream(symbol, m_queue):
        # /fapi/v1/ticker/bookTicker
        endpoint = symbol+'@bookTicker'
        # print(endpoint)
        try:
            async with websockets.connect(WS_ENDPOINT+endpoint) as ws:
                while True:
                    new_message = await ws.recv()
                    await m_queue.put(new_message)
                    await asyncio.sleep(0)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"exception binance {e}")

async def process_messages(m_queue):
    # await asyncio.sleep(2)
    while True:
        # await m_queue.get()
        print(await m_queue.get())
        # m_queue
        print("consumer")
        # print(last_message)
        await asyncio.sleep(1)

async def combine():
    message_q = asyncio.LifoQueue()
    tasks = [
        ws_get_orderbook_stream('btcusdt', message_q),
        process_messages(message_q)
    ]
    await asyncio.gather(*tasks)

# df = get_kline("BTCUSDT", "1h", "01.04.2024")

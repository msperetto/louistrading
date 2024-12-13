import pandas as pd
from common.python import management
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

class Binance():

    BASE_ENDPOINT = 'https://fapi.binance.com'
    WS_ENDPOINT = 'wss://fstream.binance.com/ws/'

    def get_servertime(self):
        request_path = '/fapi/v1/time'
        binance_out = 1
        while binance_out:
            try:
                return requests.get(self.BASE_ENDPOINT + request_path).json()['serverTime']
            except requests.exceptions.SSLError:
                print(f'Max retries exceeded with url: /api/v3/time')
                time.sleep(4)
            except Exception as e:
                print(
                    f'Binance trade server time out - sleeps 3 secs - {sys.exc_info()}')
                time.sleep(3)


    def sign_request(self, params, b_id, b_sk):
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


    def run_signed_request(self, path, params, type_req, b_id, b_sk):
        api_id = self.sign_request(params, b_id, b_sk)
        if type_req == 'get':
            binance_out = 1
            while binance_out:
                try:
                    return requests.get(self.BASE_ENDPOINT + path, params=params,
                                        headers={"X-MBX-APIKEY": api_id}).json()
                except Exception as e:
                    time.sleep(3)
                    serverTime = self.get_servertime()
                    params['timestamp'] = str(serverTime)
                    params.pop('signature')
                    self.sign_request(params, b_id, b_sk)
        else:
            binance_out = 1
            while binance_out:
                try:
                    return requests.post(self.BASE_ENDPOINT + path, params=params,
                                        headers={"X-MBX-APIKEY": api_id}).json()
                except Exception as e:
                    time.sleep(3)
                    serverTime = self.get_servertime()
                    params['timestamp'] = str(serverTime)
                    params.pop('signature')
                    self.sign_request(params, b_id, b_sk)


    def get_all_symbols(self):
        endpoint = '/fapi/v1/exchangeInfo'
        binance_out = 1

        while binance_out:
            try:
                exchange_info = requests.get(
                    self.BASE_ENDPOINT + endpoint).json()['symbols']
                binance_out = 0
            except Exception as e:
                time.sleep(1)

        result = [symbols['symbol'] for symbols in exchange_info if symbols['status'] == "TRADING"]

        
        return result

    
    async def get_orderbook(self, pairs_to_filter: list[str], pair: str = None):
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
                    exchange_info = await session.get(self.BASE_ENDPOINT + endpoint, params=params, ssl=False)
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



        # Possible intervals for klines
        # 1m
        # 3m
        # 5m
        # 15m
        # 30m
        # 1h
        # 2h
        # 4h
        # 6h
        # 8h
        # 12h
        # 1d
        # 3d
        # 1w
        # 1M
    def get_kline(self, pair: str, interval: str, startTime, endTime = round(time.time() * 1000), limit: int = 1500):
        # current time code = round(time.time() * 1000)
        endpoint = "/fapi/v1/klines"
        params = {
            "symbol": pair,
            "interval": interval,
            # "startTime": management.date_to_ms(startTime),
            'startTime': startTime,
            "endTime": endTime,
            "limit": limit
        }

        try:
            kline = requests.get(
                self.BASE_ENDPOINT + endpoint, params=params).json()
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

    def get_orderbook(self, pair, limit):
        endpoint = "/fapi/v1/depth"

        binance_out = 1

        params = {
            "symbol": pair,
            "limit": limit
        }

        while binance_out:
            try:
                orderbook = requests.get(
                    self.BASE_ENDPOINT + endpoint, params=params).json()
                binance_out = 0
            except Exception as e:
                print(e)
        
        return orderbook


    def time_intervals_to_seconds(self, interval: str) -> int:
        match interval[-1]:
            case 'm':
                return int(interval[:-1])*60
            case 'h':
                return int(interval[:-1])*3600
            case 'd':
                return int(interval[:-1])*86400
            case 'w':
                return int(interval[:-1])*604800


    def get_extended_kline(self, pair: str, interval: str, startTime: str, endTime = round(time.time() * 1000)):
        # Binance only allow 1500 max candles per request, so for longer periods of time, its necessary
        # to concatenate each request call.

        df = pd.DataFrame({})
        startTime = management.date_to_ms(startTime)
        endTime = management.date_to_ms(endTime) if isinstance(endTime, str) else endTime

        time_intervals = [startTime] # array to store all the time intervals to call the api
        
        # time in miliseconds for an specified candle interval
        startTime_offset = management.time_intervals_to_seconds(interval)*1000

        while (startTime + (startTime_offset * 1499)) < endTime:
            startTime += startTime_offset * 1499
            time_intervals.append(startTime) 
        
        time_intervals.append(endTime)
        print(time_intervals)

        for i, time_interval in enumerate(time_intervals):
            if i < len(time_intervals) -1:
                df = pd.concat([df, self.get_kline(pair, interval, time_interval + startTime_offset, time_intervals[i+1])])
        
        return df


    
    def get_bid(self, pair_info: dict):
        return pair_info["bidPrice"]


    def get_ask(self, pair_info: dict):
        return pair_info["askPrice"]


    # async def get_bid_ask(pair: str) -> list:
    #     print(get_orderbook(pair))
    #     bid = await get_orderbook(pair)["bidPrice"]
    #     ask = await get_orderbook(pair)["askPrice"]
    #     return await [bid, ask]


    async def get_mark_funding(self):
        endpoint = '/fapi/v1/premiumIndex'

        binance_out = 1

        while binance_out:
            try:
                async with aiohttp.ClientSession() as session:
                    exchange_info = await session.get(self.BASE_ENDPOINT + endpoint, ssl=False)
                    result = await exchange_info.json()
                binance_out = 0
            except Exception as e:
                print(e)
                time.sleep(1)

        return result


    def get_funding_rate_history(self, symbol, limit=100):
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
                    self.BASE_ENDPOINT + endpoint, params=params).json()
                binance_out = 0
            except Exception as e:
                time.sleep(3)

        funding_rates = self.transformUnixTimeInDatetime(funding_rates, "fundingTime")
        funding_rates = self.transformStrToFloat(funding_rates, "fundingRate")

        return funding_rates


    def transformUnixTimeInDatetime(self, entry_dict, field):
        for entry in entry_dict:
            entry[field] = str(datetime.fromtimestamp(int(entry[field]/1000)))
        return entry_dict


    def transformStrToFloat(self, entry_dict, field):
        for entry in entry_dict:
            entry[field] = float(entry[field])
        return entry_dict


    def open_position(self, symbol, amount, side, price, b_id, b_sk):
        endpoint = '/fapi/v1/order'

        params = {
            'symbol': symbol,
            'side': side, #"BUY" or "SELL"
            'type': 'LIMIT',
            'quantity': management.truncate(amount, 0),
            'price': management.truncate(price, 5),
            # IOC execute all quantity possible and cancel any remaining qtt;
            'timeInForce': 'IOC',
            'timestamp': str(self.get_servertime()),
            'recvWindow': 3000
        }
        print(f"qtt {management.truncate(amount, 0)}")
        print(f"price {management.truncate(price, 5)}")


        position = self.run_signed_request(endpoint, params, 'post', b_id, b_sk)
        if 'code' in position.keys(): # erro no servidor binance
            print(position)
            print(f'Tentativa arbitragem com erro na Binance')
        else:
            return position

    def get_open_orders(self, b_id, b_sk):
        endpoint = '/fapi/v1/openOrders'

        params = {
            'timestamp': str(self.get_servertime())
        }
        binance_out = 1
        while binance_out:
            open_orders = self.run_signed_request(endpoint, params, 'get', b_id, b_sk)
            if 'code' in open_orders.keys():
                print(f'erro get open orders {open_orders}')
            else:
                return open_orders


    def query_order(self, symbol, orderId, b_id, b_sk):
        endpoint = '/fapi/v1/order'
        params = {
            'symbol': symbol,
            'orderId': orderId,
            'recvWindow': 5000,
            'timestamp': str(self.get_servertime())
        }

        binance_out = 1
        while binance_out:
            order_info = self.run_signed_request(endpoint, params, 'get', b_id, b_sk)
            if 'code' in order_info.keys():
                print(f'erro query_order {order_info} coin: {symbol}')
            else:
                return order_info


    def account_info(self, b_id, b_sk):
        endpoint = '/fapi/v2/account'

        params = {
            'timestamp': str(self.get_servertime())
        }
        return self.run_signed_request(endpoint, params, 'get', b_id, b_sk)

    def get_bid_ask_from_ws(self, ws_response: str):
        return [ws_response["b"], ws_response["a"]]

    async def ws_get_orderbook_stream(self, symbol, m_queue):
            # /fapi/v1/ticker/bookTicker
            endpoint = symbol+'@bookTicker'
            # print(endpoint)
            try:
                async with websockets.connect(self.WS_ENDPOINT+endpoint) as ws:
                    while True:
                        new_message = await ws.recv()
                        await m_queue.put(new_message)
                        await asyncio.sleep(0)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"exception binance {e}")

    async def process_messages(self, m_queue):
        # await asyncio.sleep(2)
        while True:
            # await m_queue.get()
            print(await m_queue.get())
            # m_queue
            print("consumer")
            # print(last_message)
            await asyncio.sleep(1)

    async def combine(self):
        message_q = asyncio.LifoQueue()
        tasks = [
            self.ws_get_orderbook_stream('btcusdt', message_q),
            process_messages(message_q)
        ]
        await asyncio.gather(*tasks)

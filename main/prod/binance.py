import pandas as pd
from common import management
import time
import asyncio
from typing import List, Dict
from urllib.parse import urlencode
import hashlib
import hmac
import sys
import configparser
import requests
from datetime import datetime
import json
import logging
from common.dao import alert_dao

logger = logging.getLogger(__name__)

class Binance():

    BASE_ENDPOINT = 'https://fapi.binance.com'
    WS_ENDPOINT = 'wss://fstream.binance.com/ws/'
    TICKER_PRICE_ENDPOINT = '/fapi/v1/ticker/price'
    EXCHANGEINFO_ENDPOINT = '/fapi/v1/exchangeInfo'
    SERVERTIME_ENDPOINT = '/fapi/v1/time'
    KLINES_ENDPOINT = '/fapi/v1/klines'
    DEPTH_ENDPOINT = '/fapi/v1/depth'
    ORDER_TEST_ENDPOINT = '/fapi/v1/order/test' 
    ORDER_ENDPOINT = '/fapi/v1/order'
    OPEN_ORDER_ENDPOINT = '/fapi/v1/openOrders'
    ACCOUNT_ENDPOINT = '/fapi/v2/account'

    def get_servertime(self):
        request_path = self.SERVERTIME_ENDPOINT
        try:
            return requests.get(self.BASE_ENDPOINT + request_path).json()['serverTime']
        except requests.exceptions.SSLError:
            logger.error(f'Error getting server time: Max retries exceeded with url: /fapi/v1/time')
        except Exception as e:
            logger.error(f'Binance trade server - {sys.exc_info()} - error message {e}')


    def sign_request(self, params, b_id, b_sk):
        """given params create the signature to make any binance auth request

        Args:
            params (dict): params from any binance margin request

        Returns:
            (string): API ID of binance account
            (hmac): signature for binance request
        """
        params_binance_sign = bytes(urlencode(params), 'utf-8')
        params['signature'] = hmac.new(
            b_sk, params_binance_sign, digestmod=hashlib.sha256).hexdigest()
        return b_id


    def run_signed_request(self, path, params, type_req, b_id, b_sk):
        api_id = self.sign_request(params, b_id, b_sk)
        if type_req == 'get':
            try:
                return requests.get(self.BASE_ENDPOINT + path, params=params,
                                    headers={"X-MBX-APIKEY": api_id}).json()
            except Exception as e:
                logger.error(f'Signed request error: {e}')
                # serverTime = self.get_servertime()
                # params['timestamp'] = str(serverTime)
                # params.pop('signature')
                # self.sign_request(params, b_id, b_sk)
        else:
            try:
                return requests.post(self.BASE_ENDPOINT + path, params=params,
                                    headers={"X-MBX-APIKEY": api_id}).json()
            except Exception as e:
                logger.error(f'Signed request error: {e}')
                # serverTime = self.get_servertime()
                # params['timestamp'] = str(serverTime)
                # params.pop('signature')
                # self.sign_request(params, b_id, b_sk)


    def get_all_symbols(self):
        endpoint = self.EXCHANGEINFO_ENDPOINT

        try:
            exchange_info = requests.get(
                self.BASE_ENDPOINT + endpoint).json()['symbols']
            binance_out = 0
        except Exception as e:
            logger.error(f'Error getting all symbols: {e}')

        result = [symbols['symbol'] for symbols in exchange_info if symbols['status'] == "TRADING"]

        
        return result

    

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
        endpoint = self.KLINES_ENDPOINT
        params = {
            "symbol": pair,
            "interval": interval,
            'startTime': startTime,
            "endTime": endTime,
            "limit": limit
        }

        try:
            kline = requests.get(
                self.BASE_ENDPOINT + endpoint, params=params).json()
            binance_out = 0
        except Exception as e:
            logger.error(f'Error getting kline: {e}')
        
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
        endpoint = self.DEPTH_ENDPOINT

        params = {
            "symbol": pair,
            "limit": limit
        }

        try:
            orderbook = requests.get(
                self.BASE_ENDPOINT + endpoint, params=params).json()
            binance_out = 0
        except Exception as e:
            logger.error(f'Error getting orderbook: {e}')
        
        return orderbook

    def get_extended_kline(self, pair: str, interval: str, startTime: str, endTime = round(time.time() * 1000), period_type: str = "intraday"):
        # Binance only allow 1500 max candles per request, so for longer periods of time, its necessary
        # to concatenate each request call.

        df = pd.DataFrame({})
        startTime = management.date_to_ms(startTime)
        # time in miliseconds for an specified candle interval
        startTime_offset = management.time_intervals_to_seconds(interval)*1000

        #endtime to get all candles but the last one
        endTime = management.date_to_ms(endTime) if isinstance(endTime, str) else endTime
        if period_type == "intraday":
            endTime -= startTime_offset

        time_intervals = [startTime] # array to store all the time intervals to call the api
        

        while (startTime + (startTime_offset * 1499)) < endTime:
            startTime += startTime_offset * 1499
            time_intervals.append(startTime) 
        
        time_intervals.append(endTime)

        for i, time_interval in enumerate(time_intervals):
            if i < len(time_intervals) -1:
                df = pd.concat([df, self.get_kline(pair, interval, time_interval + startTime_offset, time_intervals[i+1])])
        
        return df

    def get_bid(self, pair_info: dict):
        return pair_info["bidPrice"]


    def get_ask(self, pair_info: dict):
        return pair_info["askPrice"]

    def get_symbol_price(self, symbol):
        endpoint = self.TICKER_PRICE_ENDPOINT

        params = {
            'symbol': symbol
        }

        try:
            return requests.get(self.BASE_ENDPOINT + endpoint, params=params).json()['price']
        except Exception as e:
            logger.error(f'Error getting symbol price: {e}')

    def open_position(self, symbol, quantity, side, b_id, b_sk):
        # TODO: Use the global NEGOCIATION_ENV to determine if it should use one or the other.
        endpoint = self.ORDER_TEST_ENDPOINT
        # endpoint = self.ORDER_ENDPOINT

        params = {
            'symbol': symbol,
            'side': side, #"BUY" or "SELL"
            'type': 'MARKET',
            'quantity': quantity,
            'timestamp': str(self.get_servertime()),
            'recvWindow': 3000
        }
        position = self.run_signed_request(endpoint, params, 'post', b_id, b_sk)
        if 'code' in position.keys(): # erro no servidor binance
            logger.error(f'Error opening position: {position}')
            alert_dao.insert_alert(symbol, "Warning", True, f"Error opening position: {position}")
        else:
            return position

    def close_position(self, symbol, side, b_id, b_sk):
        # TODO: Use the global NEGOCIATION_ENV to determine if it should use one or the other.
        endpoint = self.ORDER_TEST_ENDPOINT
        # endpoint = self.ORDER_ENDPOINT

        params = {
            'symbol': symbol,
            'side': side, #"BUY" or "SELL"
            'type': 'MARKET',
            'closePosition': True,
            'timestamp': str(self.get_servertime()),
            'recvWindow': 3000
        }
        position = self.run_signed_request(endpoint, params, 'post', b_id, b_sk)
        if 'code' in position.keys():
            logger.error(f'Error closing position: {position}')
            alert_dao.insert_alert(symbol, "Warning", True, f"Error closing position: {position}")
        else:
            return position

    def get_open_orders(self, b_id, b_sk):
        endpoint = self.OPEN_ORDER_ENDPOINT

        params = {
            'timestamp': str(self.get_servertime())
        }
        open_orders = self.run_signed_request(endpoint, params, 'get', b_id, b_sk)
        if 'code' in open_orders.keys():
            logger.error(f'Error getting open orders: {open_orders}')
        else:
            return open_orders


    def query_order(self, symbol, orderId, b_id, b_sk):
        endpoint = self.ORDER_ENDPOINT
        params = {
            'symbol': symbol,
            'orderId': orderId,
            'recvWindow': 5000,
            'timestamp': str(self.get_servertime())
        }

        order_info = self.run_signed_request(endpoint, params, 'get', b_id, b_sk)
        if 'code' in order_info.keys():
            logger.error(f'erro query_order {order_info} coin: {symbol}')
        else:
            return order_info

    def account_info(self, b_id, b_sk):
        endpoint = self.ACCOUNT_ENDPOINT

        params = {
            'timestamp': str(self.get_servertime())
        }
        return self.run_signed_request(endpoint, params, 'get', b_id, b_sk)

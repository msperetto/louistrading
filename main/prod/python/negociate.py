from prod.python.binance import Binance
from common.python import database_operations as db
import random
from datetime import datetime
class Negociate():
    environment = "TEST"
    def __init__(self, strategy, pair, api_id, api_key):
        self.pair = pair
        self.api_id = api_id
        self.api_key = api_key
    
    def open_position(self, side, total_value, strategy_id):
        if self.environment == "TEST":
            order_response = {}
            cur_price = Binance().get_orderbook(self.pair, 5) 
            order_response['orderId'] = random.randint(11111, 99999)
            order_response['updateTime'] = datetime.now()
            order_response['symbol'] = self.pair
            order_response['positionSide'] = side
            if side == "long":
                order_response['avgPrice'] = cur_price['asks'][0][0]
                order_response['origQty'] = order_response['avgPrice'] * total_value
                order_response['status'] = 'filled'
            else:
                order_response['avgPrice'] = cur_price['bids'][0][0]
                order_response['origQty'] = order_response['avgPrice'] * total_value
                order_response['status'] = 'filled'

        self.register_open_transaction(order_response, strategy_id)
        return order_response

    def close_position(self, side, total_value, strategy_id):
        if self.environment == "TEST":
            order_response = {}
            order_response['orderId'] = random.randint(11111, 99999)
            order_response['updateTime'] = datetime.now()
            order_response['symbol'] = self.pair
            order_response['positionSide'] = side
            cur_price = Binance().get_orderbook(self.pair, 5) 
            if side == "long":
                order_response['avgPrice'] = cur_price['bids'][0][0]
                order_response['origQty'] = order_response['avgPrice'] * total_value
                order_response['status'] = 'filled'
            else:
                order_response['avgPrice'] = cur_price['asks'][0][0]
                order_response['origQty'] = order_response['avgPrice'] * total_value
                order_response['status'] = 'filled'
        
        self.register_close_transaction(order_response, strategy_id)
        return order_response


    def register_open_transaction(self, order_response, strategy_id):
        db.insert_order_transaction(order_response, "Entry")
        db.insert_trade_transaction(strategy_id, True, order_response)
        
    def register_close_transaction(self, order_response, strategy_id):
        #need to calculate profit, roi ,spread
        profit = 1
        roi = 1
        spread = 1
        db.insert_order_transaction(order_response, "Close")
        db.insert_trade_transaction(strategy_id, False, order_response, profit, spread, roi)
        
    def alert_open_transaction():
        pass

    def alert_close_transaction():
        pass
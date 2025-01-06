from common.enums import Environment_Type
from prod.binance import Binance
from common.dao import database_operations as db
import random
from datetime import datetime
from config.config import NEGOCIATION_ENV

class Negociate():
    def __init__(self, pair, api_id, api_key):
        self.pair = pair
        self.api_id = api_id
        self.api_key = api_key
    
    def open_position(self, side, total_value, strategy_id):
        if NEGOCIATION_ENV == Environment_Type.TEST:
            order_response = {}
            cur_price = Binance().get_orderbook(self.pair, 5) 
            order_response['orderId'] = random.randint(11111, 99999)
            order_response['updateTime'] = datetime.now()
            order_response['symbol'] = self.pair
            order_response['positionSide'] = side
            if side == "long":
                order_response['avgPrice'] = cur_price['asks'][0][0]
                order_response['origQty'] = total_value/float(order_response['avgPrice'])
                order_response['status'] = 'filled'
            else:
                order_response['avgPrice'] = cur_price['bids'][0][0]
                order_response['origQty'] = total_value/float(order_response['avgPrice'])
                order_response['status'] = 'filled'
        
        else:
            order_quantity = total_value/float(Binance().get_symbol_price(self.pair))
            order_response = Binance().open_position(self.pair, order_quantity, side, self.api_id, self.api_key)

        self.register_open_transaction(order_response, strategy_id)
        return order_response

    def close_position(self, side, total_value, strategy_id, trade_id):
        if NEGOCIATION_ENV == Environment_Type.TEST:
            order_response = {}
            order_response['orderId'] = random.randint(11111, 99999)
            order_response['updateTime'] = datetime.now()
            order_response['symbol'] = self.pair
            order_response['positionSide'] = side
            cur_price = Binance().get_orderbook(self.pair, 5) 
            if side == "long":
                order_response['avgPrice'] = cur_price['bids'][0][0]
                order_response['origQty'] = db.get_order(trade_id)['quantity']
                order_response['status'] = 'filled'
            else:
                order_response['avgPrice'] = cur_price['asks'][0][0]
                order_response['origQty'] = db.get_order(trade_id)['quantity']
                order_response['status'] = 'filled'

        else:
            order_response = Binance().close_position(self.pair, side, self.api_id, self.api_key)
        
        self.register_close_transaction(order_response, strategy_id, trade_id)
        return order_response


    def register_open_transaction(self, order_response, strategy_id):

        trade_id = db.insert_trade_transaction(strategy_id, True, order_response)
        db.insert_order_transaction(order_response, "Entry", trade_id)
        
    def register_close_transaction(self, order_response, strategy_id, trade_id):
        entry_price = db.get_order(trade_id)['entry_price']
        entry_quantity = db.get_order(trade_id)['quantity']
        profit = (float(order_response['avgPrice'])*order_response['origQty']) - (entry_price*entry_quantity)
        spread = (float(order_response['avgPrice']) / entry_price) - 1
        #need to calculate roi
        roi = 1
        db.update_trade_transaction(trade_id, strategy_id, order_response, profit, spread, roi)
        db.insert_order_transaction(order_response, "Close", trade_id)
        
    def alert_open_transaction():
        pass

    def alert_close_transaction():
        pass

# negoc = Negociate("XTZUSDT", "a", "b")
# negoc.open_position("long", 7200, 1)
# negoc.close_position("long", 7200, 1)
from common.enums import *
from prod.binance import Binance
from common.dao import database_operations as db
import random
from datetime import datetime
from config.config import NEGOCIATION_ENV
from common.enums import Environment_Type
from prod import logger


class Negotiate():
    def __init__(self, pair, api_id, api_key):
        self.pair = pair
        self.api_id = api_id
        self.api_key = api_key
    
    def open_position(self, side, total_value, strategy_id):
        logger.info(f"Opening position: side={side}, total_value={total_value}, strategy_id={strategy_id}")

        if NEGOCIATION_ENV == Environment_Type.TEST:
            order_response = self._simulate_test_order(side, total_value)        
        else:
            order_quantity = total_value/float(Binance().get_symbol_price(self.pair))
            order_response = Binance().open_position(self.pair, order_quantity, side, self.api_id, self.api_key)

        if order_response is None:
            logger.error(f"Error opening position: {order_response}")
            return False

        self._register_open_transaction(order_response, strategy_id)
        logger.info(f"Position successfully opened: {order_response}")
        return True

    def _simulate_test_order(self, side, total_value):
        order_response = {
            'orderId': random.randint(11111, 99999),
            'updateTime': datetime.now(),
            'symbol': self.pair,
            'positionSide': side,
            'status': 'filled'
        }
        cur_price = Binance().get_orderbook(self.pair, 5)
        if side == Side_Type.LONG:
            order_response['avgPrice'] = cur_price['asks'][0][0]
        else:
            order_response['avgPrice'] = cur_price['bids'][0][0]

        order_response['origQty'] = total_value / float(order_response['avgPrice'])
        return order_response

    def close_position(self, side, total_value, strategy_id, trade_id):
        logger.info(f"Closing position: trade_id={trade_id}")
        
        if NEGOCIATION_ENV == Environment_Type.TEST:
            order_response = self._simulate_close_position(side, trade_id)
        else:
            order_response = Binance().close_position(self.pair, side, self.api_id, self.api_key)
        
        if order_response is None:
            logger.error(f"Error closing position: {order_response}")
            return False

        self._register_close_transaction(order_response, strategy_id, trade_id)
        logger.info(f"Position successfully closed: {order_response}")
        return True

    def _simulate_close_position(self, side, trade_id):
        order_response = {
            'orderId': random.randint(11111, 99999),
            'updateTime': datetime.now(),
            'symbol': self.pair,
            'positionSide': side,
            'status': 'filled'
        }
        cur_price = Binance().get_orderbook(self.pair, 5)
        trade_quantity = db.get_order(trade_id)['quantity']
        if side == Side_Type.LONG:
            order_response['avgPrice'] = cur_price['bids'][0][0]
        else:
            order_response['avgPrice'] = cur_price['asks'][0][0]

        order_response['origQty'] = trade_quantity
        return order_response

    def _register_open_transaction(self, order_response, strategy_id):
        trade_id = db.insert_trade_transaction(strategy_id, True, order_response)
        db.insert_order_transaction(order_response, Operation_Type.ENTRY, trade_id)
        #TODO: Atualizar saldo corrent do mercado futuro numa tabela nova de saldos.
        
    def _register_close_transaction(self, order_response, strategy_id, trade_id):
        # TODO: Refactor to call order_dao.get_order_by_trade_id. Ideally, it should return an "order" object.
        trade_data = db.get_order(trade_id)
        entry_price = trade_data['entry_price']
        entry_quantity = trade_data['quantity']

        # Calculates profit, spread and ROI values
        close_price = float(order_response['avgPrice'])
        close_quantity = order_response['origQty']
        profit = (close_price * close_quantity) - (entry_price * entry_quantity)
        spread = (close_price / entry_price) - 1
        roi = self._calculate_roi()

        # Updates DB tables.
        db.update_trade_transaction(trade_id, strategy_id, order_response, profit, spread, roi)
        db.insert_order_transaction(order_response, Operation_Type.CLOSE, trade_id)
        #TODO: Atualizar saldo corrent do mercado futuro numa tabela nova de saldos.
        
    # Calculates the correct ROI.    
    def _calculate_roi(self):
        # TODO: Figure out how to calculate the ROI. 
        return 1
    
    def alert_open_transaction():
        pass

    def alert_close_transaction():
        pass

# negoc = Negotiate("XTZUSDT", "a", "b")
# negoc.open_position(Side_Type.LONG, 7200, 1)
# negoc.close_position(Side_Type.LONG, 7200, 1)